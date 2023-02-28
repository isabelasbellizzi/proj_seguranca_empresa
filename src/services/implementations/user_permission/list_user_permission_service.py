from dataclasses import dataclass
from typing import List

from src.infra.repositories.interfaces import IUserPermissionRepository
from src.services.DTOs.user_permission import \
    UserPermissionResponseServiceDto,ListUserPermissionServiceRequestDTO
from src.services.implementations.user_permission.user_permission_utils import \
    UserPermissionUtils


@dataclass
class ListUserPermissionService:

    @staticmethod
    def execute(repo: IUserPermissionRepository, data: ListUserPermissionServiceRequestDTO) -> List[UserPermissionResponseServiceDto]:
        return_list: List[UserPermissionResponseServiceDto] = []
        for element in repo.get_all(data=data):
            return_list.append(UserPermissionUtils().user_permission_2_user_permission_dto(element))

        return return_list
