from dataclasses import dataclass
from src.services.DTOs.paper.update_paper_request_service_dto import UpdatePaperRequestServiceDto

@dataclass
class CreatePaperRequestServiceDto(UpdatePaperRequestServiceDto):
    system_id: int
