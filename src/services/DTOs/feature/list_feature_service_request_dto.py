from dataclasses import dataclass
from typing import Optional


@dataclass
class ListFeatureServiceRequestDTO:
    max_records: int = 0
    paper_id: Optional[int] = None
    function_id: Optional[int] = None
