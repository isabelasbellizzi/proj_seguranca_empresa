from dataclasses import dataclass
from typing import Optional
from src.domain.enums.status_enum import StatusEnum

@dataclass
class ListSystemServiceRequestDTO:
    max_records: int = 0
    system_name: Optional[str] = None
    system_status: Optional[StatusEnum] = None
