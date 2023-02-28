from dataclasses import dataclass
from src.domain.entities import Paper
from src.infra.repositories.interfaces.ipaper_repository import IPaperRepository
from src.services.exceptions import ServiceLayerNotFoundError
from src.services.DTOs.paper.paper_response_service_dto import PaperResponseServiceDto
from .paper_utils import PaperUtils


@dataclass
class GetPaperService:

    @staticmethod
    def execute(repo: IPaperRepository, paper_id: int) -> PaperResponseServiceDto:
        paper: Paper = repo.get(paper_id=paper_id)
        ServiceLayerNotFoundError.when(paper is None, f"Paper not found. [paper_id={paper_id}]")

        return PaperUtils().paper_2_paper_dto(paper)
