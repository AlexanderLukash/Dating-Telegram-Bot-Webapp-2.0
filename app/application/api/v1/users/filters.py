from pydantic import BaseModel

from app.infra.repositories.filters.users import GetAllUsersFilters


class GetUsersFilters(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetAllUsersFilters(
            limit=self.limit,
            offset=self.offset,
        )
