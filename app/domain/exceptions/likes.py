from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class InvalidUserLikeIdTypeError(ApplicationException):

    @property
    def message(self):
        return f"Invalid type for user ID."


@dataclass(eq=False)
class InvalidUserLikeIdValueError(ApplicationException):

    @property
    def message(self):
        return f"Must be a positive integer."
