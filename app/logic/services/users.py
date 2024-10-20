from dataclasses import dataclass
from typing import Iterable

from app.domain.entities.users import UserEntity
from app.domain.values.users import AboutText
from app.infra.repositories.base import BaseUsersRepository
from app.infra.repositories.filters.users import GetAllUsersFilters
from app.logic.exceptions.users import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.logic.services.base import BaseUsersService


@dataclass
class UsersService(BaseUsersService):
    user_repository: BaseUsersRepository

    async def get_user(self, telegram_id: int) -> UserEntity | None:
        user = await self.user_repository.get_user_by_telegram_id(
            telegram_id=telegram_id,
        )

        if not user:
            raise UserNotFoundException(telegram_id)

        return user

    async def check_user_is_active(self, telegram_id: int) -> bool:
        user = await self.get_user(telegram_id=telegram_id)

        if not user:
            raise UserNotFoundException(telegram_id)

        return await self.user_repository.check_user_is_active(telegram_id=telegram_id)

    async def update_user_info_after_reg(self, telegram_id: int, data: dict):
        await self.user_repository.update_user_info_after_register(
            telegram_id=telegram_id,
            data=data,
        )

    async def update_user_about_info(self, telegram_id: int, about: AboutText):
        await self.user_repository.update_user_about(
            telegram_id=telegram_id,
            about=about,
        )

    async def create_user(self, user: UserEntity) -> UserEntity:
        if await self.check_user_exist(user_id=user.telegram_id):
            raise UserAlreadyExistsException(user.telegram_id)
        await self.user_repository.create_user(user)
        return user

    async def check_user_exist(self, user_id: int) -> bool:
        return await self.user_repository.check_user_exist_by_telegram_id(
            telegram_id=user_id,
        )

    async def get_all_users(self, filters: GetAllUsersFilters) -> Iterable[UserEntity]:
        return await self.user_repository.get_all_user(filters=filters)

    async def get_users_liked_from(self, users_list: list[int]) -> Iterable[UserEntity]:
        return await self.user_repository.get_users_liked_from(user_list=users_list)

    async def get_users_liked_by(self, users_list: list[int]) -> Iterable[UserEntity]:
        return await self.user_repository.get_users_liked_by(user_list=users_list)
