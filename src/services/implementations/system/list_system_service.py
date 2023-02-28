from dataclasses import dataclass
from typing import List

from src.infra.repositories.interfaces.isystem_repository import \
    ISystemRepository
from src.services.DTOs.system import ListSystemServiceRequestDTO, SystemResponseServiceDto
from src.services.implementations.system.system_utils import SystemUtils

@dataclass
class ListSystemService:

    @staticmethod
    def execute(repo: ISystemRepository, data: ListSystemServiceRequestDTO) -> List[SystemResponseServiceDto]:
        return_list: List[SystemResponseServiceDto] = []
        for element in repo.get_all(data=data):
            return_list.append(SystemUtils().system_2_system_dto(element))

        return return_list
