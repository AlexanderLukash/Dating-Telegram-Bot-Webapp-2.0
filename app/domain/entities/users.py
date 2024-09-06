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
    name: Name
    username: str | None = None
    gender: Gender | None = None
    age: Age | None = None
    city: City | None = None
    looking_for: Gender | None = None
    about: AboutText | None = None
    is_active: bool = False
