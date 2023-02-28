from dataclasses import dataclass

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import IFeatureRepository
from src.services.DTOs.feature import UpdateFeatureRequestServiceDto
from src.services.exceptions import ServiceLayerNotFoundError


@dataclass
class UpdateFeatureService:
    @staticmethod
    def execute(db: IDbHandler, repo: IFeatureRepository, feature_id: int, data: UpdateFeatureRequestServiceDto) -> None:
        feature = repo.get(id=feature_id)
        ServiceLayerNotFoundError.when(feature is None, f"Feature not found. [feature_id={feature_id}]")

        if data.create is not None:
            feature.create = data.create
        if data.read is not None:
            feature.read = data.read
        if data.update is not None:
            feature.update = data.update
        if data.delete is not None:
            feature.delete = data.delete

        feature.validate()

        repo.update(feature)
        db.commit()
