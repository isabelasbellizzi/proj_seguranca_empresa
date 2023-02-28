from dataclasses import dataclass

from src.services.DTOs.feature import UpdateFeatureRequestServiceDto


@dataclass
class CreateFeatureRequestServiceDto(UpdateFeatureRequestServiceDto):
    paper_id: int
    function_id: int
