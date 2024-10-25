from punq import Container
from pytest import fixture

from app.infra.repositories.base import (
    BaseLikesRepository,
    BaseUsersRepository,
)
from app.logic.services.base import (
    BaseLikesService,
    BaseUsersService,
)
from app.tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture()
def users_repository(container: Container) -> BaseUsersRepository:
    return container.resolve(BaseUsersRepository)


@fixture()
def likes_repository(container: Container) -> BaseLikesRepository:
    return container.resolve(BaseLikesRepository)


@fixture()
def users_service(container: Container) -> BaseUsersService:
    return container.resolve(BaseUsersService)


@fixture()
def likes_service(container: Container) -> BaseLikesService:
    return container.resolve(BaseLikesService)
