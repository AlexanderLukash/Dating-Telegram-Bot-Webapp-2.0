from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from aiogram.types import User

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
    username: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[Age] = None
    city: Optional[City] = None
    looking_for: Optional[Gender] = None
    about: Optional[AboutText] = None
    photo: Optional[str] = None
    is_active: bool = False

    @classmethod
    def from_telegram_user(cls, user: User) -> "UserEntity":
        return cls(
            telegram_id=user.id,
            username=user.username or "",
            name=Name(user.first_name),
            created_at=datetime.now()
        )
