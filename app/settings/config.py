from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    token: str = Field(alias="BOT_TOKEN")
    url_webhook: str = Field(alias="WEBHOOK_URL")

    @property
    def full_webhook_url(self) -> str:
        return f"{self.url_webhook}/api/v1/webhook"
