from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import uuid4


@dataclass
class BaseEntity(ABC):
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
