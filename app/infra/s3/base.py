from abc import (
    ABC,
    abstractmethod,
)


class BaseS3Storage(ABC):
    @abstractmethod
    async def upload_file(self, file: bytes, file_name: str) -> str: ...
