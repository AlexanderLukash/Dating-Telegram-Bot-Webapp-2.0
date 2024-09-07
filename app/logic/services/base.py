from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.domain.entities.users import UserEntity


@dataclass
class BaseUsersService(ABC):
    @abstractmethod
    async def create_user(self, user: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def check_user_exist(self, user_id: int): ...
