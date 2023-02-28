from dataclasses import dataclass

from src.domain.enums.function_type_enum import FunctionTypeEnum


@dataclass
class UpdateFunctionRequestServiceDto():
    name: str
    function_type: FunctionTypeEnum
