from dataclasses import dataclass
from src.domain.enums.status_enum import StatusEnum
from src.services.DTOs.paper.create_paper_request_service_dto import CreatePaperRequestServiceDto


@dataclass
class PaperResponseServiceDto(CreatePaperRequestServiceDto):
    paper_id: int
    name_system: str
    status: StatusEnum
