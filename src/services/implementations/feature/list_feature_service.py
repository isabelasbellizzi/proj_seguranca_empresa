from dataclasses import dataclass
from typing import List

from src.infra.repositories.interfaces import IFeatureRepository
from src.services.DTOs.feature import FeatureResponseServiceDto
from src.services.implementations.feature.feature_utils import FeatureUtils
from src.services.DTOs.feature import ListFeatureServiceRequestDTO


@dataclass
class ListFeatureService:
    @staticmethod
    def execute(repo: IFeatureRepository, data: ListFeatureServiceRequestDTO) -> List[FeatureResponseServiceDto]:
        return_list: List[FeatureResponseServiceDto] = []
        for element in repo.get_all(data=data):
            return_list.append(FeatureUtils().feature_2_feature_dto(element))

        return return_list
