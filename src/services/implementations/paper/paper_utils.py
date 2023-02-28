from dataclasses import dataclass

from src.domain.entities.paper import Paper
from src.services.DTOs.paper.paper_response_service_dto import PaperResponseServiceDto

@dataclass
class PaperUtils:
    @staticmethod
    def paper_2_paper_dto(ori: Paper) -> PaperResponseServiceDto:
        return PaperResponseServiceDto(
            paper_id=ori.paper_id,
            system_id=ori.system_id,
            name=ori.name,
            name_system=ori.system.system_name,
            status=ori.status
        )
