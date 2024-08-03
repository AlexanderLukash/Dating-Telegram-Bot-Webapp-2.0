from dataclasses import dataclass
from typing import Literal

from app.domain.exceptions.users import (
    AboutTextTooLongException,
    AboutTextTooShortException,
    AgeNotInRangeException,
    CityTooShortException,
    EmptyAgeException,
    EmptyCityException,
    EmptyNameException,
    NameTooLongException,
    NameTooShortException,
)
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Name(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyNameException()

        if len(self.value) > 50:
            raise NameTooLongException(self.value)

        if len(self.value) == 1:
            raise NameTooShortException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Age(BaseValueObject):
    value: int

    def validate(self):
        if not self.value:
            raise EmptyAgeException()

        if self.value <= 10 or self.value >= 120:
            raise AgeNotInRangeException(self.value)

    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class City(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyCityException()

        if len(self.value) == 1:
            raise CityTooShortException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Gender(BaseValueObject):
    value: str | Literal["Man", "Female"]

    def validate(self):
        if self.value not in ["Man", "Female"]:
            raise ValueError(f"Invalid gender: {self.value}")

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class AboutText(BaseValueObject):
    value: str | None

    def validate(self):
        if len(self.value) > 125:
            raise AboutTextTooLongException(self.value)

        if len(self.value) < 3:
            raise AboutTextTooShortException(self.value)

    def as_generic_type(self) -> str | None:
        return str(self.value)
