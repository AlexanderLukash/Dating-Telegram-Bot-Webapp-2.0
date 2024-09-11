from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserAlreadyExistsException(LogicException):
    telegram_id: int

    @property
    def message(self):
        return "User already exists."


@dataclass(eq=False)
class UserNotFoundException(LogicException):
    telegram_id: int

    @property
    def message(self):
        return f"User with this id: '{self.telegram_id}' not found."
