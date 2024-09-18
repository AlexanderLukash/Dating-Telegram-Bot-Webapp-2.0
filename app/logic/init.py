from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from app.infra.repositories.base import BaseUsersRepository
from app.infra.repositories.mongo import MongoDBUserRepository
from app.infra.s3.base import BaseS3Storage
from app.infra.s3.storage import (
    BaseS3Client,
    S3Storage,
)
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

    def create_s3_client() -> BaseS3Client:
        return BaseS3Client(
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            bucket_name=config.bucket_name,
            region_name=config.region_name,
        )

    container.register(
        BaseS3Client,
        factory=create_s3_client,
        scope=Scope.singleton,
    )

    def init_s3_storage() -> S3Storage:
        s3_client = container.resolve(BaseS3Client)

        return S3Storage(
            aws_access_key_id=s3_client.aws_access_key_id,
            aws_secret_access_key=s3_client.aws_secret_access_key,
            bucket_name=s3_client.bucket_name,
            region_name=s3_client.region_name,
        )

    container.register(
        BaseS3Storage,
        factory=init_s3_storage,
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
