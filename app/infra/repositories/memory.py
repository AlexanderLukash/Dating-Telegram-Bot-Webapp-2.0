from dataclasses import dataclass
from typing import Iterable

from app.domain.entities.likes import LikesEntity
from app.domain.entities.users import UserEntity
from app.domain.values.users import AboutText
from app.infra.repositories.base import (
    BaseLikesRepository,
    BaseUsersRepository,
)
from app.infra.repositories.filters.users import GetAllUsersFilters


@dataclass
class MemoryUsersRepository(BaseUsersRepository):
    _users = {}

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity | None:
        return self._users.get(telegram_id)

    async def check_user_is_active(self, telegram_id: int) -> bool:
        user = self._users.get(telegram_id)
        return user.is_active if user else False

    async def update_user_info_after_register(self, telegram_id: int, data: dict):
        user = self._users.get(telegram_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)

    async def update_user_about(self, telegram_id: int, about: AboutText):
        user = self._users.get(telegram_id)
        if user:
            user.about = about

    async def create_user(self, user: UserEntity):
        self._users[user.telegram_id] = user

    async def check_user_exist_by_telegram_id(self, telegram_id: int) -> bool:
        return telegram_id in self._users

    async def get_all_user(
        self,
        filters: GetAllUsersFilters,
    ) -> tuple[Iterable[UserEntity], int]:
        all_users = list(self._users.values())
        return all_users[filters.offset : filters.offset + filters.limit], len(
            all_users,
        )

    async def get_users_liked_from(self, user_list: list[int]) -> Iterable[UserEntity]:
        return [user for user in self._users.values() if user.telegram_id in user_list]

    async def get_users_liked_by(self, user_list: list[int]) -> Iterable[UserEntity]:
        return [user for user in self._users.values() if user.telegram_id in user_list]


class MemoryLikesRepository(BaseLikesRepository):
    def __init__(self):
        self.likes = {}

    async def check_like_is_exists(self, from_user_id: int, to_user_id: int) -> bool:
        return (from_user_id, to_user_id) in self.likes

    async def create_like(self, like: LikesEntity):
        self.likes[(like.from_user.value, like.to_user.value)] = like

    async def delete_like(self, from_user: int, to_user: int):
        if (from_user, to_user) in self.likes:
            del self.likes[(from_user, to_user)]

    async def get_users_ids_liked_from(self, user_id: int) -> list[int]:
        return [
            to_user
            for (from_user, to_user) in self.likes.keys()
            if from_user == user_id
        ]

    async def get_users_ids_liked_by(self, user_id: int) -> list[int]:
        return [
            from_user
            for (from_user, to_user) in self.likes.keys()
            if to_user == user_id
        ]
