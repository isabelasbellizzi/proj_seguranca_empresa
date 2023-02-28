from dataclasses import dataclass
from src.domain.entities.user import User
from src.services.DTOs.user.user_response_service_dto import UserResponseServiceDto


@dataclass
class UserUtilis:
    @staticmethod
    def user_2_user_dto(ori: User) -> UserResponseServiceDto:
        return UserResponseServiceDto(
            user_id=ori.user_id,  # type: ignore
            azure_id=ori.azure_id,  # type: ignore
            user_email=ori.user_email,
            status=ori.status
        )
