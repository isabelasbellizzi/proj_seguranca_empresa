from dataclasses import dataclass

from src.domain.entities import Function
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import (IFunctionRepository,
                                               ISystemRepository)
from src.services.DTOs.function.create_function_request_service_dto import \
    CreateFunctionRequestServiceDto
from src.services.exceptions import (ServiceLayerDuplicatedNameError,
                                     ServiceLayerNotFoundError)
from src.services.implementations.function.function_utils import FunctionUtils


@dataclass
class InsertFunctionService:

    @staticmethod
    def execute(db: IDbHandler, repo: IFunctionRepository, system_repo: ISystemRepository, data: CreateFunctionRequestServiceDto):
        new_function = Function(**data.__dict__)
        new_function.validate()

        system_read = system_repo.get(system_id=new_function.system_id)
        ServiceLayerNotFoundError.when(system_read is None, f"System not found. [system_id={new_function.system_id}]")

        function_read = repo.get_byname(name=new_function.name)
        ServiceLayerDuplicatedNameError.when(function_read is not None, f"This function name already exists. [function_name={new_function.name}]")

        repo.add(new_function)
        db.commit()

        return FunctionUtils().function_2_function_dto(new_function)
