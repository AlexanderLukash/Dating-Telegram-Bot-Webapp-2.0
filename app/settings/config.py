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

    aws_access_key_id: str = Field(
        alias="AWS_ACCESS_KEY_ID",
    )
    aws_secret_access_key: str = Field(
        alias="AWS_SECRET_ACCESS_KEY",
    )
    bucket_name: str = Field(
        alias="S3_BUCKET_NAME",
    )
    region_name: str = Field(
        default="us-east-1",
        alias="S3_REGION_NAME",
    )

    @property
    def full_webhook_url(self) -> str:
        return f"{self.url_webhook}/api/v1/webhook"

    front_end_url: str = Field(alias="FRONT_END_URL")
