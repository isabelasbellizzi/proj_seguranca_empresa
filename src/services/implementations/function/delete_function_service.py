from dataclasses import dataclass
from typing import List

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import \
    IFunctionRepository, IFeatureRepository
from src.services.exceptions import \
    ServiceLayerNotFoundError, ServiceLayerForeignKeyError
from src.domain.entities import Feature
from src.services.DTOs.feature import ListFeatureServiceRequestDTO


@dataclass
class DeleteFunctionService:

    @staticmethod
    def execute(db: IDbHandler, repo: IFunctionRepository, feature_repo: IFeatureRepository, id: int) -> None:
        function_read = repo.get(id=id)
        ServiceLayerNotFoundError.when(function_read is None, f"Function not found. [function_id={id}]")
        
        feature_read: List[Feature] = feature_repo.get_all(data=ListFeatureServiceRequestDTO(function_id=id))
        ServiceLayerForeignKeyError.when(len(feature_read) > 0, f"Function has features. [function_id={id}]")

        repo.delete(id=id)
        db.commit()
