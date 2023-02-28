from dataclasses import dataclass
from typing import List

from src.infra.repositories.interfaces.ifunction_repository import \
    IFunctionRepository
from src.services.DTOs.function.function_response_service_dto import \
    FunctionResponseServiceDto
from src.services.DTOs.function.list_function_service_request_dto import \
    ListFunctionServiceRequestDTO

from .function_utils import FunctionUtils


@dataclass
class ListFunctionService:

    @staticmethod
    def execute(repo: IFunctionRepository, data: ListFunctionServiceRequestDTO) -> List[FunctionResponseServiceDto]:
        return_list: List[FunctionResponseServiceDto] = []
        for element in repo.get_all(data=data):
            return_list.append(FunctionUtils().function_2_function_dto(element))

        return return_list
