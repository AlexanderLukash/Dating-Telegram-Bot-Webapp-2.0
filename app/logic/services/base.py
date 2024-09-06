from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseUsersService(ABC):
    @abstractmethod
    def create_user(self, user_data): ...
