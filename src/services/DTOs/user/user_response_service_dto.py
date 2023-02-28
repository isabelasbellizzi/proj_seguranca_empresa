from dataclasses import dataclass

from src.domain.enums.status_enum import StatusEnum
from src.services.DTOs.user.update_user_request_service_dto import \
    UpdateUserRequestServiceDto


@dataclass
class UserResponseServiceDto(UpdateUserRequestServiceDto):
    user_id: int
    status: StatusEnum
