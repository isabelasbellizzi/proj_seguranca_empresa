from dataclasses import dataclass
from typing import Optional
from src.domain.enums.status_enum import StatusEnum

@dataclass
class ListPaperServiceRequestDTO:
    max_records: int = 0
    system_id: Optional[int] = None
    paper_name: Optional[str] = None
    paper_status: Optional[StatusEnum] = None
