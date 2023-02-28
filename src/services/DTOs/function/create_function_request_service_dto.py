from dataclasses import dataclass

from src.services.DTOs.function.update_function_request_service_dto import \
    UpdateFunctionRequestServiceDto


@dataclass
class CreateFunctionRequestServiceDto(UpdateFunctionRequestServiceDto):
    system_id: int
