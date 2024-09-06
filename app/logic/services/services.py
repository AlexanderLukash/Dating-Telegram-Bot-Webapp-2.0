from dataclasses import dataclass

from app.domain.entities.users import UserEntity
from app.infra.repositories.base import BaseUsersRepository
from app.logic.services.base import BaseUsersService


@dataclass
class UsersService(BaseUsersService):
    user_repository: BaseUsersRepository

    async def create_user(self, user: UserEntity) -> UserEntity:
        # Створюємо новий об'єкт користувача на основі вхідних даних

        # Викликаємо метод репозиторію для створення користувача
        await self.user_repository.create_user(user)

        return user
