from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.likes import Like


@dataclass
class LikesEntity(BaseEntity):
    from_user: Like
    to_user: Like
