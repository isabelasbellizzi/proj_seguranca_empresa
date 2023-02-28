from dataclasses import dataclass

from src.domain.entities.system import System
from src.services.DTOs.system.system_response_service_dto import \
    SystemResponseServiceDto


@dataclass
class SystemUtils:
    @staticmethod
    def system_2_system_dto(ori: System) -> SystemResponseServiceDto:
        return SystemResponseServiceDto(
            system_id=ori.system_id,
            token_id=ori.token_id,
            system_name=ori.system_name,
            status=ori.status
        )
