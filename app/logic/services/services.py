from dataclasses import dataclass

from app.domain.entities.users import UserEntity
from app.infra.repositories.base import BaseUsersRepository
from app.logic.exceptions.user import UserAlreadyExistsException
from app.logic.services.base import BaseUsersService


@dataclass
class UsersService(BaseUsersService):
    user_repository: BaseUsersRepository

    async def create_user(self, user: UserEntity) -> UserEntity:
        if await self.check_user_exist(user_id=user.telegram_id):
            raise UserAlreadyExistsException(user.telegram_id)
        await self.user_repository.create_user(user)
        return user

    async def check_user_exist(self, user_id: int) -> bool:
        return await self.user_repository.check_user_exist_by_telegram_id(
            telegram_id=user_id,
        )
