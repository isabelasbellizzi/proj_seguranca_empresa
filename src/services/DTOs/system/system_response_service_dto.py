from dataclasses import dataclass

from src.domain.enums.status_enum import StatusEnum
from src.services.DTOs.system.create_system_request_service_dto import \
    CreateSystemRequestServiceDto


@dataclass
class SystemResponseServiceDto (CreateSystemRequestServiceDto):  # pylint: disable=too-few-public-methods
    system_id: int
    status: StatusEnum
