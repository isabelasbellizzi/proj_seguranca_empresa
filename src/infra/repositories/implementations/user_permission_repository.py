from typing import List, Optional

from src.domain.entities import UserPermission
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.iuser_permission_repository import \
    IUserPermissionRepository
from src.services.DTOs.user_permission import \
    ListUserPermissionServiceRequestDTO


class UserPermissionRepository(IUserPermissionRepository):
    def __init__(self, db: IDbHandler):
        self.session = db.get_session()

    def get(self, user_permission_id: int) -> Optional[UserPermission]:
        query = self.session.query(UserPermission).filter(UserPermission.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(UserPermission.user_permission_id == user_permission_id)
        return query.first()

    def get_all(self, data: ListUserPermissionServiceRequestDTO) -> List[UserPermission]:
        query = self.session.query(UserPermission).filter(UserPermission.status != StatusEnum.LOGICALLYDELETED)

        if data.paper_id is not None:
            query = query.filter(UserPermission.paper_id == data.paper_id)

        if data.user_id is not None:
            query = query.filter(UserPermission.user_id == data.user_id)

        if data.max_records > 0:
            query = query.limit(data.max_records)

        return query.all()

    def add(self, new_user_permission: UserPermission) -> None:
        new_user_permission.validate()
        new_user_permission.status = StatusEnum.ACTIVE
        new_user_permission.user_permission_id = None # type: ignore
        self.session.add(new_user_permission)
        self.session.flush()

    def delete(self, user_permission_id: int) -> None:
        user_permission = self.get(user_permission_id=user_permission_id)

        if not user_permission:
            raise Exception(f"User Permission not found. [user_permission_id={user_permission_id}]")

        user_permission.status = StatusEnum.LOGICALLYDELETED
        self.session.flush()

    def update(self, user_permission: UserPermission) -> None:
        user_permission.validate()
        self.session.flush()
