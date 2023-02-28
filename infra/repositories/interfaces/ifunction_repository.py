from typing import Any, List, Optional

from src.domain.entities.function import Function
from src.infra.repositories.interfaces.icrud_repository import ICrudRepository
from src.services.DTOs.function.list_function_service_request_dto import \
    ListFunctionServiceRequestDTO


class IFunctionRepository(ICrudRepository):
    def get_byname(self, name: str, id_exc: int = 0) -> Optional[Function]:
        raise Exception("Not Implemented")

    def get_all(self, data: ListFunctionServiceRequestDTO) -> List[Any]:
        raise Exception("Not Implemented")
