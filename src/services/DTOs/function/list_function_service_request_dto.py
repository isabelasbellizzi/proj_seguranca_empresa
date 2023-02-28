from dataclasses import dataclass
from typing import Optional
from src.domain.enums.function_type_enum import FunctionTypeEnum


@dataclass
class ListFunctionServiceRequestDTO:
    max_records: int = 0
    system_id: Optional[int] = None
    function_name: Optional[str] = None
    function_type: Optional[FunctionTypeEnum] = None
