from dataclasses import dataclass

from app.domain.exceptions.likes import InvalidUserLikeIdTypeError, InvalidUserLikeIdValueError
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Like(BaseValueObject):
    value: int

    def validate(self):
        if not isinstance(self.value, int):
            raise InvalidUserLikeIdTypeError()

        if self.value <= 0:
            raise InvalidUserLikeIdValueError()

    def as_generic_type(self) -> int:
        return self.value
