from dataclasses import dataclass


@dataclass
class GetAllUsersFilters:
    limit: int = 10
    offset: int = 0
