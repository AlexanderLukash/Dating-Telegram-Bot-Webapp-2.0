from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from app.domain.entities.users import UserEntity


@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserEntity): ...
