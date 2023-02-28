from typing import List
from dataclasses import dataclass
from src.domain.entities import UserPermission
from src.domain.entities import Owner

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.iuser_repository import IUserRepository
from src.infra.repositories.interfaces.iuser_permission_repository import IUserPermissionRepository
from src.infra.repositories.interfaces.iowner_repository import IOwnerRepository
from src.services.exceptions.service_layer_foreign_key_error import ServiceLayerForeignKeyError
from src.services.exceptions.service_layer_notfound_error import ServiceLayerNotFoundError
from src.services.DTOs.user_permission import ListUserPermissionServiceRequestDTO
from src.services.DTOs.owner import ListOwnerServiceRequestDTO


@dataclass
class DeleteUserService:

    @staticmethod
    def execute(db: IDbHandler, repo: IUserRepository, up_repo: IUserPermissionRepository, owner_repo:IOwnerRepository, user_id: int) -> None:

        user_read = repo.get_by_user_id(user_id=user_id)
        ServiceLayerNotFoundError.when(user_read is None, f"User not found. [user_id={user_id}]")
        
        if (user_read is None):
            raise Exception(f"User not found. [user_id={user_id}]")
        
        up_read: List[UserPermission] = up_repo.get_all(data=ListUserPermissionServiceRequestDTO(user_id=user_id))
        ServiceLayerForeignKeyError.when(len(up_read) > 0, f"User has permissions. [user_id={user_id}]")
        
        owner_read: List[Owner] = owner_repo.get_all(data=ListOwnerServiceRequestDTO(user_id=user_id))
        ServiceLayerForeignKeyError.when(len(owner_read) > 0, f"User is an owner [user_id={user_id}]")

        
       
        

        repo.delete(user_id=user_id)
        db.commit()
