from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.domain.entities.likes import LikesEntity
from app.domain.entities.users import UserEntity
from app.domain.values.users import AboutText
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
    async def update_user_info_after_register(self, telegram_id: int, data: dict): ...

    @abstractmethod
    async def update_user_about(self, telegram_id: int, about: AboutText): ...

    @abstractmethod
    async def create_user(self, user: UserEntity): ...

    @abstractmethod
    async def check_user_exist_by_telegram_id(self, telegram_id: int) -> bool: ...


@dataclass
class BaseLikesRepository(ABC):
    @abstractmethod
    async def check_like_is_exists(self, from_user: int, to_user: int) -> bool: ...

    @abstractmethod
    async def get_users_liked_from(self, user_id: int): ...

    @abstractmethod
    async def get_user_liked_by(self, user_id: int): ...

    @abstractmethod
    async def create_like(self, like: LikesEntity) -> LikesEntity: ...

    @abstractmethod
    async def delete_like(self, from_user: int, to_user: int): ...
