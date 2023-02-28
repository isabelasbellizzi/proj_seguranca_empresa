from dataclasses import dataclass
from typing import List
from src.infra.repositories.interfaces.ipaper_repository import IPaperRepository
from src.services.DTOs.paper.paper_response_service_dto import PaperResponseServiceDto
from src.services.DTOs.paper.list_paper_service_request_dto import \
    ListPaperServiceRequestDTO
from .paper_utils import PaperUtils

@dataclass
class ListPaperService:

    @staticmethod
    def execute(repo: IPaperRepository, data: ListPaperServiceRequestDTO) -> List[PaperResponseServiceDto]:
        return_list: List[PaperResponseServiceDto] = []
        for element in repo.get_all(data=data):
            return_list.append(PaperUtils().paper_2_paper_dto(element))
        return return_list
