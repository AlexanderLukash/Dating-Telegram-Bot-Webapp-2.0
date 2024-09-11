from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.domain.entities.users import UserEntity
from app.infra.repositories.filters.users import GetAllUsersFilters


@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity: ...

    @abstractmethod
    async def check_user_is_active(self, telegram_id: int) -> bool: ...

    @abstractmethod
    async def get_all_user(self, filters: GetAllUsersFilters): ...

    @abstractmethod
    async def create_user(self, user: UserEntity): ...

    @abstractmethod
    async def check_user_exist_by_telegram_id(self, telegram_id: int) -> bool: ...
