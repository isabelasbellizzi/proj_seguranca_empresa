from dataclasses import dataclass

from src.infra.repositories.interfaces.ifunction_repository import \
    IFunctionRepository
from src.services.DTOs.function.function_response_service_dto import \
    FunctionResponseServiceDto
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError

from .function_utils import FunctionUtils


@dataclass
class GetFunctionService:

    @staticmethod
    def execute(repo: IFunctionRepository, id: int) -> FunctionResponseServiceDto:
        function = repo.get(id=id)
        ServiceLayerNotFoundError.when(function is None, f"Function not found. [function_id={id}]")

        return FunctionUtils().function_2_function_dto(function)
