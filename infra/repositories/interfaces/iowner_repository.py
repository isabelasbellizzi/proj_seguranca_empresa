
from abc import ABC, abstractmethod
from typing import Any, List
from src.domain.entities import Owner
from src.services.DTOs.owner import \
ListOwnerServiceRequestDTO
class IOwnerRepository(ABC):

    @abstractmethod
    def get(self, id: int) -> Any:
        raise Exception("Not implemented")

    @abstractmethod
    def get_all(self, data: ListOwnerServiceRequestDTO) -> List[Any]:
        raise Exception("Not implemented")

    @abstractmethod
    def add(self, new: Owner) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def delete(self, id: int) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def update(self, obj: Owner) -> None:
        raise Exception("Not implemented")
