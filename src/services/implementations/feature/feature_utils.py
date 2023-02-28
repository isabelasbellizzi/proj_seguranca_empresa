from dataclasses import dataclass

from src.domain.entities import Feature
from src.services.DTOs.feature.feature_response_service_dto import \
    FeatureResponseServiceDto


@dataclass
class FeatureUtils:
    @staticmethod
    def feature_2_feature_dto(ori: Feature) -> FeatureResponseServiceDto:
        return FeatureResponseServiceDto(
            create=ori.create,
            read=ori.read,
            update=ori.update,
            delete=ori.delete,
            paper_id=ori.paper_id,
            function_id=ori.function_id,
            feature_id=ori.feature_id,
            paper_name=ori.paper.name,
            function_name=ori.function.name,
            system_name=ori.paper.system.system_name,
            status=ori.status
        )
