from datetime import datetime

from pydantic import BaseModel

from app.domain.entities.likes import LikesEntity


class CreateLikeRequestSchema(BaseModel):
    from_user: int
    to_user: int


class CreateLikeResponseSchema(BaseModel):
    from_user: int
    to_user: int
    created_at: datetime

    @classmethod
    def from_entity(cls, like: LikesEntity) -> "CreateLikeResponseSchema":
        return CreateLikeResponseSchema(
            from_user=like.from_user.as_generic_type(),
            to_user=like.to_user.as_generic_type(),
            created_at=like.created_at,
        )
