from dataclasses import dataclass

from src.domain.enums.status_enum import StatusEnum
from src.services.DTOs.feature.create_feature_request_service_dto import CreateFeatureRequestServiceDto


@dataclass
class FeatureResponseServiceDto(CreateFeatureRequestServiceDto):
    feature_id: int
    paper_name: str
    function_name: str
    system_name: str
    status: StatusEnum
