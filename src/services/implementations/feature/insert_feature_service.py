from dataclasses import dataclass
from typing import List

from src.domain.entities import Feature
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import (IFeatureRepository,
                                               IFunctionRepository,
                                               IPaperRepository)
from src.services.DTOs.feature import CreateFeatureRequestServiceDto, ListFeatureServiceRequestDTO
from src.services.exceptions import (ServiceLayerNotFoundError, ServiceLayerDuplicatedObjectError)
from src.services.implementations.feature.feature_utils import FeatureUtils


@dataclass
class InsertFeatureService:
    @staticmethod
    def execute(db: IDbHandler, repo: IFeatureRepository, function_repo: IFunctionRepository, paper_repo: IPaperRepository, data: CreateFeatureRequestServiceDto):
        new_feature = Feature(**data.__dict__)
        new_feature.validate()

        function_read = function_repo.get(id=new_feature.function_id)
        ServiceLayerNotFoundError.when(function_read is None, f"Function not found. [function_id={new_feature.function_id}]")

        paper_read = paper_repo.get(paper_id=new_feature.paper_id)
        ServiceLayerNotFoundError.when(paper_read is None, f"Paper not found. [paper_id={new_feature.paper_id}]")

        list_feature_request_dto = ListFeatureServiceRequestDTO(paper_id=new_feature.paper_id, function_id=new_feature.function_id)

        feature_read: List[Feature] = repo.get_all(data=list_feature_request_dto)
        if len(feature_read) > 0:
            raise ServiceLayerDuplicatedObjectError(f"A feature with this paper_id and this function_id already exists. [feature_id={feature_read[0].feature_id}]")

        repo.add(new_feature)
        db.commit()

        return FeatureUtils().feature_2_feature_dto(new_feature)
