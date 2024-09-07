from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.domain.entities.users import UserEntity


@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserEntity): ...

    @abstractmethod
    async def check_user_exist_by_telegram_id(self, telegram_id: int) -> bool: ...
