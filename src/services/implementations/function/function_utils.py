from dataclasses import dataclass

from src.domain.entities.function import Function
from src.services.DTOs.function.function_response_service_dto import \
    FunctionResponseServiceDto


@dataclass
class FunctionUtils:
    @staticmethod
    def function_2_function_dto(ori: Function) -> FunctionResponseServiceDto:
        return FunctionResponseServiceDto(
            function_id=ori.function_id,
            system_id=ori.system_id,
            name=ori.name,
            name_system=ori.system.system_name,
            function_type=ori.function_type,
            status=ori.status
        )
