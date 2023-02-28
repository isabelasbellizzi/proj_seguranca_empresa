from dataclasses import dataclass

from src.domain.entities import Owner
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import (IOwnerRepository,
                                               ISystemRepository,
                                               IUserRepository)
from src.services.DTOs.owner import CreateOwnerRequestServiceDto, ListOwnerServiceRequestDTO, OwnerResponseServiceDto
from src.services.exceptions import (ServiceLayerDuplicatedObjectError,
                                     ServiceLayerNotFoundError)
from src.services.implementations.owner.owner_utils import OwnerUtils


@dataclass
class InsertOwnerService:

    @staticmethod
    def execute(db: IDbHandler, repo: IOwnerRepository, system_repo: ISystemRepository, user_repo: IUserRepository, data: CreateOwnerRequestServiceDto) -> OwnerResponseServiceDto:
        new_owner = Owner(**data.__dict__)
        new_owner.validate()

        system_read = system_repo.get(system_id=new_owner.system_id)
        ServiceLayerNotFoundError.when(system_read is None, f"System not found. [system_id={new_owner.system_id}]")

        user_read = user_repo.get_by_user_id(user_id=new_owner.user_id)
        ServiceLayerNotFoundError.when(user_read is None, f"User not found. [user_id={new_owner.user_id}]")

        list_data = ListOwnerServiceRequestDTO(system_id=new_owner.system_id, user_id=new_owner.user_id)

        owner_read = repo.get_all(data=list_data)
        if len(owner_read) != 0:
            raise ServiceLayerDuplicatedObjectError(f"This owner already exists. [owner_id={owner_read[0].owner_id}]")

        repo.add(new_owner)
        db.commit()

        return OwnerUtils().owner_2_owner_dto(new_owner)
