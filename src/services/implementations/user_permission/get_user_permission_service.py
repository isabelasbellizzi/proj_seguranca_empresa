from dataclasses import dataclass

from src.domain.entities import UserPermission
from src.infra.repositories.interfaces import IUserPermissionRepository
from src.services.DTOs.user_permission.user_permission_response_service_dto import \
    UserPermissionResponseServiceDto
from src.services.exceptions import ServiceLayerNotFoundError

from .user_permission_utils import UserPermissionUtils


@dataclass
class GetUserPermissionService:

    @staticmethod
    def execute(repo: IUserPermissionRepository, user_permission_id: int) -> UserPermissionResponseServiceDto:
        user_permission: UserPermission = repo.get(user_permission_id=user_permission_id)
        ServiceLayerNotFoundError.when(user_permission is None, f"User permission id not found. [user permission id={user_permission_id}]")

        return UserPermissionUtils().user_permission_2_user_permission_dto(user_permission)
