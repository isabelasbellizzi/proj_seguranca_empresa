from dataclasses import dataclass
from typing import List

from src.infra.repositories.interfaces import IOwnerRepository, ISystemRepository, IUserRepository
from src.services.DTOs.owner.list_owner_service_request_dto import ListOwnerServiceRequestDTO
from src.services.DTOs.system.system_response_service_dto import SystemResponseServiceDto
from src.services.exceptions.service_layer_notfound_error import ServiceLayerNotFoundError
from src.services.implementations.system import SystemUtils



@dataclass
class GetSystemsOwnedService:
    @staticmethod
    def execute(repo: IOwnerRepository, system_repo: ISystemRepository, user_repo: IUserRepository, user_email:str) -> List[SystemResponseServiceDto]:
        user = user_repo.get_by_email(user_email=user_email)
        ServiceLayerNotFoundError.when(user is None, f"User not found. [user_email={user_email}")

        data = ListOwnerServiceRequestDTO(user_id=user.user_id)
        owner_list = repo.get_all(data=data)

        ServiceLayerNotFoundError.when(len(owner_list) == 0, f"This user does not own a system. [user_id={user.user_id}]")

        system_list = []
        for owner in owner_list:
            system = system_repo.get(system_id=owner.system_id)
            system_list.append(SystemUtils.system_2_system_dto(system))  # type: ignore

        return system_list
