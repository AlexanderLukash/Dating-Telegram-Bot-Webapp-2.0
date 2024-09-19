from abc import ABC
from contextlib import asynccontextmanager
from dataclasses import dataclass

from aiobotocore.session import get_session

from app.infra.s3.base import BaseS3Storage
from app.settings.config import Config


config: Config = Config()


@dataclass
class BaseS3Client(ABC):
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket_name: str
    region_name: str
    session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as client:
            yield client


class S3Storage(BaseS3Storage, BaseS3Client):
    async def upload_file(self, file: bytes, file_name: str) -> str:
        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket_name, Key=file_name, Body=file)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
