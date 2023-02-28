from dataclasses import dataclass
from typing import List

from src.infra.repositories.interfaces import ISystemPermissionRepository, ISystemRepository
from src.services.exceptions import ServiceLayerNotFoundError
from src.services.DTOs.system_permission import SystemPermissionResponseServiceDTO, PermissionDTO


@dataclass
class ListSystemPermissionService:
    @staticmethod
    def execute(repo: ISystemPermissionRepository, system_repo: ISystemRepository, system_id: int) -> List[SystemPermissionResponseServiceDTO]:
        system_read = system_repo.get(system_id=system_id)
        ServiceLayerNotFoundError.when(system_read is None, f"System not found. [system_id={system_id}]")

        system_permission_dicts = repo.get_all(system_id=system_id)
        system_permissions: List[SystemPermissionResponseServiceDTO] = []

        for system_permission_dict in system_permission_dicts:
            permission = PermissionDTO(paper_id=system_permission_dict["paper_id"], paper_name=system_permission_dict["paper_name"])

            existing_user = False
            for system_permission in system_permissions:
                if system_permission.user_id == system_permission_dict["user_id"]:
                    existing_user = True
                    system_permission.permissions.append(permission)

            if existing_user is False or len(system_permissions) == 0:
                response_dto = SystemPermissionResponseServiceDTO(user_id=system_permission_dict["user_id"], user_email=system_permission_dict["user_email"], permissions=[permission])
                system_permissions.append(response_dto)

        return system_permissions
