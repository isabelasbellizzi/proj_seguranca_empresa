from dataclasses import dataclass

from src.domain.entities import UserPermission
from src.services.DTOs.user_permission.user_permission_response_service_dto import \
    UserPermissionResponseServiceDto


@dataclass
class UserPermissionUtils:

    @staticmethod
    def user_permission_2_user_permission_dto(ori: UserPermission) -> UserPermissionResponseServiceDto:
        return UserPermissionResponseServiceDto(
            user_permission_id=ori.user_permission_id,
            user_id=ori.user_id,
            user_email=ori.user.user_email,
            paper_id=ori.paper_id,
            paper_name=ori.paper.name,
            status=ori.status
        )
