from abc import ABC
from dataclasses import dataclass
from typing import Iterable

from motor.core import AgnosticClient

from app.domain.entities.likes import LikesEntity
from app.domain.entities.users import UserEntity
from app.domain.values.users import AboutText
from app.infra.repositories.base import (
    BaseLikesRepository,
    BaseUsersRepository,
)
from app.infra.repositories.converters import (
    convert_like_entity_to_document,
    convert_user_document_to_entity,
    convert_user_entity_to_document,
)
from app.infra.repositories.filters.users import GetAllUsersFilters


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBUserRepository(BaseUsersRepository, BaseMongoDBRepository):
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity | None:
        user_document = await self._collection.find_one(
            filter={"telegram_id": telegram_id},
        )

        if not user_document:
            return None

        return convert_user_document_to_entity(user_document=user_document)

    async def check_user_is_active(self, telegram_id: int) -> bool:
        user_document = await self._collection.find_one(
            filter={"telegram_id": telegram_id, "is_active": True},
        )

        return bool(user_document)

    async def update_user_info_after_register(self, telegram_id: int, data: dict):
        await self._collection.update_one(
            filter={"telegram_id": telegram_id},
            update={"$set": data},
        )

    async def update_user_about(self, telegram_id: int, about: AboutText):
        await self._collection.update_one(
            filter={"telegram_id": telegram_id},
            update={"$set": {"about": about.as_generic_type()}},
        )

    async def create_user(self, user: UserEntity):
        await self._collection.insert_one(convert_user_entity_to_document(user))

    async def check_user_exist_by_telegram_id(self, telegram_id: int) -> bool:
        return bool(
            await self._collection.find_one(
                filter={"telegram_id": telegram_id},
            ),
        )

    async def get_all_user(
        self,
        filters: GetAllUsersFilters,
    ) -> tuple[Iterable[UserEntity], int]:
        cursor = self._collection.find().skip(filters.offset).limit(filters.limit)

        count = await self._collection.count_documents({})
        chats = [
            convert_user_document_to_entity(user_document=user_document)
            async for user_document in cursor
        ]

        return chats, count

    async def get_best_result_for_user(self, telegram_id: int) -> Iterable[UserEntity]:
        user = await self.get_user_by_telegram_id(telegram_id)
        if user is None:
            return []

        user_age = user.age
        user_city = user.city

        age_min = int(user_age) - 3
        age_max = int(user_age) + 3

        users_documents = self._collection.find(
            filter={
                "city": user_city,
                "telegram_id": {"$ne": telegram_id},
                "$expr": {
                    "$and": [
                        {"$gte": [{"$toInt": "$age"}, age_min]},
                        {"$lte": [{"$toInt": "$age"}, age_max]},
                    ],
                },
            },
        )

        # Конвертуємо документи у сутності
        return [
            convert_user_document_to_entity(user_document=user_document)
            async for user_document in users_documents
        ]

    async def get_users_liked_from(self, user_list: list[int]) -> Iterable[UserEntity]:
        users_documents = self._collection.find(
            filter={"telegram_id": {"$in": user_list}},
        )

        result = []
        async for user_document in users_documents:
            telegram_id = user_document.get("telegram_id")
            if telegram_id:
                user_entity = await self.get_user_by_telegram_id(
                    telegram_id=telegram_id,
                )
                if user_entity:
                    result.append(user_entity)

        return result

    async def get_users_liked_by(self, user_list: list[int]) -> Iterable[UserEntity]:
        users_documents = self._collection.find(
            filter={"telegram_id": {"$in": user_list}},
        )

        result = []
        async for user_document in users_documents:
            telegram_id = user_document.get("telegram_id")
            if telegram_id:
                user_entity = await self.get_user_by_telegram_id(
                    telegram_id=telegram_id,
                )
                if user_entity:
                    result.append(user_entity)

        return result


@dataclass
class MongoDBLikesRepository(BaseLikesRepository, BaseMongoDBRepository):
    async def check_like_is_exists(self, from_user: int, to_user: int) -> bool:
        return bool(
            await self._collection.find_one(
                filter={
                    "from_user": from_user,
                    "to_user": to_user,
                },
            ),
        )

    async def create_like(self, like: LikesEntity) -> LikesEntity:
        await self._collection.insert_one(convert_like_entity_to_document(like))
        return like

    async def delete_like(self, from_user: int, to_user: int):
        await self._collection.delete_one(
            filter={
                "from_user": from_user,
                "to_user": to_user,
            },
        )

    async def get_users_ids_liked_from(self, user_id: int) -> list[int]:
        users_documents = self._collection.find(
            filter={"from_user": user_id},
        )

        result = []
        async for user_document in users_documents:
            telegram_id = user_document.get("to_user")
            if telegram_id:
                result.append(telegram_id)

        return result

    async def get_users_ids_liked_by(self, user_id: int) -> list[int]:
        users_documents = self._collection.find(
            filter={"to_user": user_id},
        )

        result = []
        async for user_document in users_documents:
            telegram_id = user_document.get("from_user")
            if telegram_id:
                result.append(telegram_id)

        return result
