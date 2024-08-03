from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.users import (
    AboutText,
    Age,
    City,
    Gender,
    Name,
)


@dataclass
class UserEntity(BaseEntity):
    telegram_id: int
    username: str | None
    name: Name
    gender: Gender
    age: Age
    city: City
    looking_for: Gender
    about: AboutText
    is_active: bool
