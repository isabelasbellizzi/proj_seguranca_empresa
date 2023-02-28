from dataclasses import dataclass
from typing import List

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import IPaperRepository, IUserPermissionRepository,IFeatureRepository
from src.services.exceptions import \
        ServiceLayerNotFoundError, ServiceLayerForeignKeyError
from src.domain.entities import (UserPermission,Feature)
from src.services.DTOs.user_permission import ListUserPermissionServiceRequestDTO
from src.services.DTOs.feature import ListFeatureServiceRequestDTO

@dataclass
class DeletePaperService:

    @staticmethod
    def execute(db: IDbHandler, repo: IPaperRepository, user_per_repo: IUserPermissionRepository, feature_repo: IFeatureRepository, paper_id: int) -> None:

        user_permission_read: List[UserPermission] = user_per_repo.get_all(data=ListUserPermissionServiceRequestDTO(paper_id=paper_id))
        ServiceLayerForeignKeyError.when(len(user_permission_read) > 0,f"Paper has User permissions. [paper_id={paper_id}]")

        feature_read: List[Feature] = feature_repo.get_all(data=ListFeatureServiceRequestDTO(paper_id=paper_id))
        ServiceLayerForeignKeyError.when(len(feature_read) > 0,f"Paper has Feature. [paper_id={paper_id}]")

        paper_read = repo.get(paper_id=paper_id)
        ServiceLayerNotFoundError.when(paper_read is None, f"paper not found. [paper_id={paper_id}]")

        repo.delete(paper_id=paper_id)
        db.commit()
