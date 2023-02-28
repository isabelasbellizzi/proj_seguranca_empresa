from abc import ABC, abstractmethod
from typing import Any, List
from src.domain.entities import Feature
from src.services.DTOs.feature import ListFeatureServiceRequestDTO

class IFeatureRepository(ABC):

    @abstractmethod
    def get(self, id: int) -> Any:
        raise Exception("Not implemented")

    @abstractmethod
    def get_all(self, data: ListFeatureServiceRequestDTO) -> List[Any]:
        raise Exception("Not implemented")

    @abstractmethod
    def add(self, new: Feature) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def delete(self, id: int) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def update(self, obj: Feature) -> None:
        raise Exception("Not implemented")
