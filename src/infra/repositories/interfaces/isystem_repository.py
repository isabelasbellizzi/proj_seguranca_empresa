from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.system import System
from src.services.DTOs.system import ListSystemServiceRequestDTO


class ISystemRepository(ABC):
    @abstractmethod
    def get_byname(self, system_name: str, id_exc: int = 0) -> System:
        raise Exception("Not implemented")

    @abstractmethod
    def get(self, system_id: int) -> Optional[System]:
        raise Exception("Not implemented")

    @abstractmethod
    def get_all(self, data: ListSystemServiceRequestDTO) -> List[System]:
        raise Exception("Not implemented")

    @abstractmethod
    def add(self, new: System) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def delete(self, system_id: int) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def update(self, obj: System) -> None:
        raise Exception("Not implemented")
