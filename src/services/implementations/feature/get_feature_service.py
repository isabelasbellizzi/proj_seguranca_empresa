from dataclasses import dataclass

from src.infra.repositories.interfaces.ifeature_repository import \
    IFeatureRepository
from src.services.DTOs.feature.feature_response_service_dto import \
    FeatureResponseServiceDto
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError
from src.services.implementations.feature.feature_utils import FeatureUtils


@dataclass
class GetFeatureService:
    @staticmethod
    def execute(repo: IFeatureRepository, id: int) -> FeatureResponseServiceDto:
        feature = repo.get(id=id)
        ServiceLayerNotFoundError.when(feature is None, f"Feature not found. [feature_id={id}]")

        return FeatureUtils().feature_2_feature_dto(feature)
