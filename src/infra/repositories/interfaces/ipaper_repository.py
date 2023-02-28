
from abc import ABC, abstractmethod
from typing import Any, List,Optional
from src.domain.entities.paper import Paper
from src.services.DTOs.paper.list_paper_service_request_dto import \
    ListPaperServiceRequestDTO

class IPaperRepository(ABC):
    @abstractmethod
    def get_byname(self, name: str, id_exc: int = 0) -> Optional[Paper]:
        raise Exception("Not implemented")

    @abstractmethod
    def get(self, paper_id: int) -> Any:
        raise Exception("Not implemented")

    @abstractmethod
    def get_all(self, data: ListPaperServiceRequestDTO) -> List[Any]:
        raise Exception("Not implemented")

    @abstractmethod
    def add(self, new: Paper) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def delete(self, paper_id: int) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def update(self, obj: Paper) -> None:
        raise Exception("Not implemented")
