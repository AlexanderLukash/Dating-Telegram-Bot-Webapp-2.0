from abc import ABC
from dataclasses import dataclass

from aiobotocore.client import AioBaseClient

from app.infra.s3.base import BaseS3Storage


@dataclass
class S3Client(ABC):
    s3_storage_client: AioBaseClient


class S3Storage(BaseS3Storage, S3Client): ...
