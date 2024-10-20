from dataclasses import dataclass

from app.bot.utils.notificator import send_liked_message
from app.domain.entities.likes import LikesEntity
from app.domain.values.likes import Like
from app.infra.repositories.base import BaseLikesRepository
from app.logic.exceptions.likes import (
    LikeAlreadyExistsException,
    LikeIsNotExistsException,
    LikeTheSameUserException,
)
from app.logic.services.base import BaseLikesService


@dataclass
class LikesService(BaseLikesService):
    like_repository: BaseLikesRepository

    async def check_match(self, from_user_id: int, to_user_id: int) -> bool:
        if await self.like_repository.check_like_is_exists(
            from_user_id,
            to_user_id,
        ) and await self.like_repository.check_like_is_exists(
            to_user_id,
            from_user_id,
        ):
            return True
        return False

    async def create_like(self, from_user_id: int, to_user_id: int) -> LikesEntity:
        if await self.like_repository.check_like_is_exists(from_user_id, to_user_id):
            raise LikeAlreadyExistsException()

        from_user = Like(value=from_user_id)
        to_user = Like(value=to_user_id)

        if from_user == to_user:
            raise LikeTheSameUserException()

        new_like = LikesEntity(
            from_user=from_user,
            to_user=to_user,
        )
        await self.like_repository.create_like(new_like)
        if await self.check_match(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
        ):
            await send_liked_message(from_user_id, to_user_id)
        return new_like

    async def delete_like(self, from_user_id: int, to_user_id: int):
        if await self.like_repository.check_like_is_exists(from_user_id, to_user_id):
            await self.like_repository.delete_like(
                from_user=from_user_id,
                to_user=to_user_id,
            )

        else:
            raise LikeIsNotExistsException()

    async def get_telegram_id_liked_from(self, user_id: int) -> list[int]:
        telegram_ids = await self.like_repository.get_users_ids_liked_from(
            user_id=user_id,
        )
        return telegram_ids

    async def get_users_ids_liked_by(self, user_id: int) -> list[int]:
        telegram_ids = await self.like_repository.get_users_ids_liked_by(
            user_id=user_id,
        )
        return telegram_ids
