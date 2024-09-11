from dataclasses import dataclass

from app.domain.entities.users import UserEntity
from app.infra.repositories.base import BaseUsersRepository
from app.infra.repositories.filters.users import GetAllUsersFilters
from app.logic.exceptions.user import (
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

    async def create_user(self, user: UserEntity) -> UserEntity:
        if await self.check_user_exist(user_id=user.telegram_id):
            raise UserAlreadyExistsException(user.telegram_id)
        await self.user_repository.create_user(user)
        return user

    async def check_user_exist(self, user_id: int) -> bool:
        return await self.user_repository.check_user_exist_by_telegram_id(
            telegram_id=user_id,
        )

    async def get_all_users(self, filters: GetAllUsersFilters):
        return await self.user_repository.get_all_user(filters=filters)
