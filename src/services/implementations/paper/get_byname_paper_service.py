from dataclasses import dataclass
from typing import Optional
from src.domain.entities.paper import Paper
from src.infra.repositories.interfaces.ipaper_repository import IPaperRepository
from src.services.exceptions.service_layer_notfound_error import ServiceLayerNotFoundError

@dataclass
class GetByNamePaperService:

    @staticmethod
    def execute(repo: IPaperRepository, paper_name: str) -> Optional[Paper]:
        paper = repo.get_byname(name=paper_name)
        ServiceLayerNotFoundError.when(paper is None, f"Paper not found. [paper_name={paper_name}]")

        return paper
