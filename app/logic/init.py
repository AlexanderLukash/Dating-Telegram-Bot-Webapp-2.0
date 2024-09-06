from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from app.infra.repositories.base import BaseUsersRepository
from app.infra.repositories.mongo import MongoDBUserRepository
from app.logic.services.base import BaseUsersService
from app.logic.services.services import UsersService
from app.settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    config: Config = container.resolve(Config)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.mongodb_connection_uri,
            serverSelectionTimeoutMS=3000,
        )

    container.register(
        AsyncIOMotorClient,
        factory=create_mongodb_client,
        scope=Scope.singleton,
    )
    client = container.resolve(AsyncIOMotorClient)

    def init_users_mongodb_repository() -> BaseUsersRepository:
        return MongoDBUserRepository(
            mongo_db_client=client,
            mongo_db_name=config.mongodb_dating_database,
            mongo_db_collection_name=config.mongodb_users_collection,
        )

    container.register(
        BaseUsersRepository,
        factory=init_users_mongodb_repository,
        scope=Scope.singleton,
    )

    def init_users_service() -> UsersService:
        return UsersService(user_repository=container.resolve(BaseUsersRepository))

    container.register(
        BaseUsersService,
        factory=init_users_service,
        scope=Scope.singleton,
    )

    return container
