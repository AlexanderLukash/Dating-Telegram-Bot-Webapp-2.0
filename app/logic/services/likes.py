from dataclasses import dataclass

from app.domain.entities.likes import LikesEntity
from app.domain.values.likes import Like
from app.infra.repositories.base import BaseLikesRepository
from app.logic.exceptions.likes import (
    LikeAlreadyExistsException,
    LikeTheSameUserException,
)
from app.logic.services.base import BaseLikesService


@dataclass
class LikesService(BaseLikesService):
    like_repository: BaseLikesRepository

    async def create_like(self, from_user_id: int, to_user_id: int) -> LikesEntity:
        if await self.like_repository.check_like_is_exists(from_user_id, to_user_id):
            raise LikeAlreadyExistsException()

        from_user = Like(value=from_user_id)
        to_user = Like(value=to_user_id)

        if from_user == to_user:
            raise LikeTheSameUserException()

        new_like = LikesEntity(from_user=from_user, to_user=to_user)
        await self.like_repository.create_like(new_like)
        return new_like
