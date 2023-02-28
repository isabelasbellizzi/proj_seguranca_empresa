from dataclasses import dataclass
from typing import List

from src.infra.repositories.interfaces import \
    IOwnerRepository
from src.services.DTOs.owner import \
    OwnerResponseServiceDto, ListOwnerServiceRequestDTO

from src.services.implementations.owner.owner_utils import OwnerUtils


@dataclass
class ListOwnerService:

    @staticmethod
    def execute(repo: IOwnerRepository, data: ListOwnerServiceRequestDTO) -> List[OwnerResponseServiceDto]:
        return_list: List[OwnerResponseServiceDto] = []
        for element in repo.get_all(data=data):
            return_list.append(OwnerUtils().owner_2_owner_dto(element))

        return return_list
