from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.domain.entities.users import UserEntity
from app.infra.repositories.filters.users import GetAllUsersFilters


@dataclass
class BaseUsersService(ABC):
    @abstractmethod
    async def create_user(self, user: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def check_user_exist(self, user_id: int): ...

    @abstractmethod
    async def get_user(self, telegram_id: int) -> UserEntity: ...

    @abstractmethod
    async def update_user_info_after_reg(self, telegram_id: int, data: dict): ...

    @abstractmethod
    async def check_user_is_active(self, telegram_id: int) -> bool: ...

    @abstractmethod
    async def get_all_users(self, filters: GetAllUsersFilters): ...
