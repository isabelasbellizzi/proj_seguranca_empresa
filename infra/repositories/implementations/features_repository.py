from typing import List, Optional
from src.domain.entities import Feature
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.ifeature_repository import IFeatureRepository
from src.services.DTOs.feature import ListFeatureServiceRequestDTO

class FeatureRepository(IFeatureRepository):
    def __init__(self, db: IDbHandler):
        self.session = db.get_session()

    def get(self, id: int) -> Optional[Feature]:
        query = self.session.query(Feature).filter(Feature.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(Feature.feature_id == id)
        return query.first()

    def get_all(self, data: ListFeatureServiceRequestDTO) -> List[Feature]:
        query = self.session.query(Feature).filter(Feature.status != StatusEnum.LOGICALLYDELETED)

        if data.paper_id is not None:
            query = query.filter(Feature.paper_id == data.paper_id)

        if data.function_id is not None:
            query = query.filter(Feature.function_id == data.function_id)

        if data.max_records > 0:
            query = query.limit(data.max_records)

        return query.all()

    def add(self, new_feature: Feature) -> None:
        new_feature.validate()
        new_feature.status = StatusEnum.ACTIVE
        new_feature.feature_id = None  # type: ignore
        self.session.add(new_feature)
        self.session.flush()

    def delete(self, id: int) -> None:
        feature = self.get(id=id)

        if not feature:
            raise Exception(f"Feature not found. [feature_id={id}]")

        feature.status = StatusEnum.LOGICALLYDELETED
        self.session.flush()

    def update(self, feature: Feature) -> None:
        feature.validate()
        self.session.flush()
