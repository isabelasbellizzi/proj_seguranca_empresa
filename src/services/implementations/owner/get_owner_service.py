from dataclasses import dataclass

from src.infra.repositories.interfaces import IOwnerRepository
from src.services.exceptions.service_layer_notfound_error import ServiceLayerNotFoundError
from src.services.implementations.owner.owner_utils import OwnerUtils
from src.services.DTOs.owner import OwnerResponseServiceDto


@dataclass
class GetOwnerService:
    @staticmethod
    def execute(repo: IOwnerRepository, owner_id:int) -> OwnerResponseServiceDto:
        owner = repo.get(id=owner_id)
        ServiceLayerNotFoundError.when(owner is None, f"Owner not found. [owner_id={owner_id}]")

        return OwnerUtils().owner_2_owner_dto(owner)
