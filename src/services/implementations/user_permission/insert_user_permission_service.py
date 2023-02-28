from dataclasses import dataclass
from typing import List

from src.domain.entities import UserPermission
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import (IPaperRepository,
                                               IUserPermissionRepository,
                                               IUserRepository)
from src.services.DTOs.user_permission import \
    CreateUserPermissionRequestServiceDto,ListUserPermissionServiceRequestDTO,UserPermissionResponseServiceDto
from src.services.exceptions import ServiceLayerNotFoundError,ServiceLayerDuplicatedObjectError
from src.services.implementations.user_permission import UserPermissionUtils


@dataclass
class InsertUserPermissionService:

    @staticmethod
    def execute(db: IDbHandler, repo: IUserPermissionRepository, paper_repo: IPaperRepository, user_repo: IUserRepository, data: CreateUserPermissionRequestServiceDto)->List[UserPermissionResponseServiceDto]:

        user_read = user_repo.get_by_user_id(user_id=data.user_id)
        ServiceLayerNotFoundError.when(user_read is None, f"user_id not found. [user_id={data.user_id}]")

        list_new_paper: List[UserPermissionResponseServiceDto] = []

        duplicated_paper_id_list: List[int] = []

        for paper in data.paper_id:
            paper_id = paper_repo.get(paper_id=paper)
            ServiceLayerNotFoundError.when(paper_id is None, f"paper_id not found. [paper_id={paper}]")

            user_permission_read: List[UserPermission] = repo.get_all(data=ListUserPermissionServiceRequestDTO(user_id=data.user_id, paper_id=paper))
            if len(user_permission_read) > 0:
                duplicated_paper_id_list.append(user_permission_read[0].paper_id)
                continue

            new_user_permission = UserPermission(user_id=data.user_id, paper_id=paper)
            new_user_permission.validate()

            repo.add(new_user_permission)
            list_new_paper.append(UserPermissionUtils().user_permission_2_user_permission_dto(new_user_permission))

        ServiceLayerDuplicatedObjectError.when(len(duplicated_paper_id_list) > 0, f"User [user_id={data.user_id}] already has permissions [paper_ids: {duplicated_paper_id_list}].")

        db.commit()

        return list_new_paper
