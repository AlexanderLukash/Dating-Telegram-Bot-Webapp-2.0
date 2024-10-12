from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(eq=False)
class LikeAlreadyExistsException(LogicException):
    @property
    def message(self):
        return "Like already exists."


@dataclass(eq=False)
class LikeTheSameUserException(LogicException):
    @property
    def message(self):
        return "Like from the same user."


@dataclass(eq=False)
class LikeIsNotExistsException(LogicException):
    @property
    def message(self):
        return "Like does not exist."
