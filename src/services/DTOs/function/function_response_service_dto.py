from dataclasses import dataclass

from src.domain.enums.status_enum import StatusEnum
from src.services.DTOs.function.create_function_request_service_dto import \
    CreateFunctionRequestServiceDto


@dataclass
class FunctionResponseServiceDto(CreateFunctionRequestServiceDto):
    function_id: int
    name_system: str
    status: StatusEnum
