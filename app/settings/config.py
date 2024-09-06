from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    token: str = Field(alias="BOT_TOKEN")
    url_webhook: str = Field(alias="WEBHOOK_URL")

    mongodb_connection_uri: str = Field(alias="MONGO_DB_CONNECTION_URI")
    mongodb_dating_database: str = Field(
        default="dating",
        alias="MONGO_DB_DATING_DATABASE",
    )
    mongodb_users_collection: str = Field(
        default="users",
        alias="MONGO_DB_USERS_COLLECTION",
    )
    mongodb_likes_collection: str = Field(
        default="likes",
        alias="MONGO_DB_LIKES_COLLECTION",
    )

    @property
    def full_webhook_url(self) -> str:
        return f"{self.url_webhook}/api/v1/webhook"
