from dataclasses import dataclass
from src.domain.enums.status_enum import StatusEnum
from src.services.DTOs.owner import CreateOwnerRequestServiceDto


@dataclass
class OwnerResponseServiceDto(CreateOwnerRequestServiceDto):
    owner_id:int
    user_email: str
    system_name: str
    status: StatusEnum
