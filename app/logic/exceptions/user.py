from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserAlreadyExistsException(LogicException):
    telegram_id: int

    @property
    def message(self):
        return "User already exists."
