from dataclasses import dataclass

from src.services.DTOs.user.update_user_request_service_dto import \
    UpdateUserRequestServiceDto


@dataclass
class CreateUserRequestServiceDto(UpdateUserRequestServiceDto):
    pass
