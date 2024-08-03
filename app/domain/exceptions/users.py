from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class EmptyNameException(ApplicationException):
    @property
    def message(self):
        return "Name cannot be empty."


@dataclass(eq=False)
class NameTooLongException(ApplicationException):
    name: str

    @property
    def message(self):
        return f"Name is too long '{self.name[:50]}...'."


@dataclass(eq=False)
class NameTooShortException(ApplicationException):
    name: str

    @property
    def message(self):
        return f"Name is too short '{self.name}'."


@dataclass(eq=False)
class EmptyAgeException(ApplicationException):
    @property
    def message(self):
        return "Age cannot be empty."


@dataclass(eq=False)
class AgeNotInRangeException(ApplicationException):
    age: int

    @property
    def message(self):
        return f"Age '{self.age}' is not in the valid range (10-120)."


@dataclass(eq=False)
class EmptyCityException(ApplicationException):
    @property
    def message(self):
        return "City cannot be empty."


@dataclass(eq=False)
class CityTooShortException(ApplicationException):
    city: str

    @property
    def message(self):
        return f"City '{self.city}' is too short."


@dataclass(eq=False)
class AboutTextTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"About text is too long '{self.text[:50]}...'."


@dataclass(eq=False)
class AboutTextTooShortException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"About text is too short '{self.text}'."
