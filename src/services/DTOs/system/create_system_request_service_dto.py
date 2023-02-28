from dataclasses import dataclass

from src.services.DTOs.system.update_system_request_service_dto import \
    UpdateSystemRequestServiceDto


@dataclass
class CreateSystemRequestServiceDto(UpdateSystemRequestServiceDto):
    pass
