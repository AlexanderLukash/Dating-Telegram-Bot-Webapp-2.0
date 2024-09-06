from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient

from app.domain.entities.users import UserEntity
from app.infra.repositories.base import BaseUsersRepository
from app.infra.repositories.converters import convert_user_entity_to_document


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
    async def create_user(self, user: UserEntity):
        await self._collection.insert_one(convert_user_entity_to_document(user))
