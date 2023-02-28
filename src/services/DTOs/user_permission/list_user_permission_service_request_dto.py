from dataclasses import dataclass
from typing import Optional


@dataclass
class ListUserPermissionServiceRequestDTO:
    max_records: int = 0
    user_id: Optional[int] = None
    paper_id: Optional[int] = None
