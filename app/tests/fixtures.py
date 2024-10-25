from punq import (
    Container,
    Scope,
)

from app.infra.repositories.base import (
    BaseLikesRepository,
    BaseUsersRepository,
)
from app.infra.repositories.memory import (
    MemoryLikesRepository,
    MemoryUsersRepository,
)
from app.infra.s3.base import BaseS3Storage
from app.logic.init import _init_container
from app.logic.services.base import (
    BaseLikesService,
    BaseUsersService,
)
from app.logic.services.likes import LikesService
from app.logic.services.users import UsersService


def init_dummy_container() -> Container:
    container = _init_container()

    container.register(
        BaseUsersRepository,
        MemoryUsersRepository,
        scope=Scope.singleton,
    )

    container.register(
        BaseLikesRepository,
        MemoryLikesRepository,
        scope=Scope.singleton,
    )

    container.register(
        BaseS3Storage,
        scope=Scope.singleton,
    )

    def init_users_service() -> UsersService:
        return UsersService(user_repository=container.resolve(BaseUsersRepository))

    def init_likes_service() -> LikesService:
        return LikesService(like_repository=container.resolve(BaseLikesRepository))

    container.register(
        BaseUsersService,
        factory=init_users_service,
        scope=Scope.singleton,
    )

    container.register(
        BaseLikesService,
        factory=init_likes_service,
        scope=Scope.singleton,
    )

    return container
