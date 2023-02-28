from dataclasses import dataclass

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.ifeature_repository import IFeatureRepository
from src.services.exceptions.service_layer_notfound_error import ServiceLayerNotFoundError


@dataclass
class DeleteFeatureService:

    @staticmethod
    def execute(db: IDbHandler, repo: IFeatureRepository, feature_id: int) -> None:
        feature_read = repo.get(id=feature_id)
        ServiceLayerNotFoundError.when(feature_read is None, f"Feature not found. [feature_id={feature_id}]")

        repo.delete(id=feature_id)
        db.commit()
