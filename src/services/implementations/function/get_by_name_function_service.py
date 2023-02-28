from dataclasses import dataclass
from typing import Optional

from src.domain.entities.function import Function
from src.infra.repositories.interfaces.ifunction_repository import \
    IFunctionRepository
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError


@dataclass
class GetByNameFunctionService:

    @staticmethod
    def execute(repo: IFunctionRepository, name: str) -> Optional[Function]:
        function = repo.get_byname(name=name)
        ServiceLayerNotFoundError.when(function is None, f"Function not found. [function_name={name}]")

        return function
