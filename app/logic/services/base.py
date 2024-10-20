from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from app.domain.entities.likes import LikesEntity
from app.domain.entities.users import UserEntity
from app.domain.values.users import AboutText
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
    async def update_user_about_info(self, telegram_id: int, about: AboutText): ...

    @abstractmethod
    async def check_user_is_active(self, telegram_id: int) -> bool: ...

    @abstractmethod
    async def get_all_users(self, filters: GetAllUsersFilters): ...

    @abstractmethod
    async def get_users_liked_from(
        self,
        users_list: list[int],
    ) -> Iterable[UserEntity]: ...

    @abstractmethod
    async def get_users_liked_by(
        self,
        users_list: list[int],
    ) -> Iterable[UserEntity]: ...


@dataclass
class BaseLikesService(ABC):
    @abstractmethod
    async def create_like(self, from_user_id: int, to_user_id: int) -> LikesEntity: ...

    @abstractmethod
    async def delete_like(self, from_user_id: int, to_user_id: int): ...

    @abstractmethod
    async def get_telegram_id_liked_from(self, user_id: int) -> list[int]: ...

    @abstractmethod
    async def get_users_ids_liked_by(self, user_id: int) -> list[int]: ...

    @abstractmethod
    async def check_match(self, from_user_id: int, to_user_id: int) -> bool: ...
