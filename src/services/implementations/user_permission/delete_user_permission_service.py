from dataclasses import dataclass

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import IUserPermissionRepository
from src.services.exceptions.service_layer_notfound_error import ServiceLayerNotFoundError


@dataclass
class DeleteUserPermissionService:

    @staticmethod
    def execute(db: IDbHandler, repo: IUserPermissionRepository, user_permission_id: int) -> None:
        user_read = repo.get(user_permission_id=user_permission_id)
        ServiceLayerNotFoundError.when(user_read is None, f"User permission id not found. [user permission id={user_permission_id}]")

        repo.delete(user_permission_id=user_permission_id)
        db.commit()
