from typing import Optional

from pydantic import BaseModel

from app.application.api.schemas import BaseQueryResponseSchema
from app.domain.entities.users import UserEntity


class UserDetailSchema(BaseModel):
    telegram_id: int
    name: str
    username: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    city: Optional[str]
    looking_for: Optional[str]
    about: Optional[str]
    is_active: bool

    @classmethod
    def from_entity(cls, user: UserEntity) -> "UserDetailSchema":
        return UserDetailSchema(
            telegram_id=user.telegram_id,
            name=user.name,
            username=user.username,
            gender=user.gender,
            age=user.age,
            city=user.city,
            looking_for=user.looking_for,
            about=user.about,
            is_active=user.is_active,
        )


class GetUsersResponseSchema(BaseQueryResponseSchema):
    items: list[UserDetailSchema]


class GetUsersFromResponseSchema(BaseModel):
    items: list[UserDetailSchema]
