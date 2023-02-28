from dataclasses import dataclass
from typing import Optional
from src.domain.enums import StatusEnum


@dataclass
class ListOwnerServiceRequestDTO:
    max_records: int = 0
    system_id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[StatusEnum] = None
