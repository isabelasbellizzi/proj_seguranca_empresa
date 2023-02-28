from dataclasses import dataclass

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import IFunctionRepository
from src.services.DTOs.function.update_function_request_service_dto import \
    UpdateFunctionRequestServiceDto
from src.services.exceptions import (ServiceLayerDuplicatedNameError,
                                     ServiceLayerNotFoundError)


@dataclass
class UpdateFunctionService:

    @staticmethod
    def execute(db: IDbHandler, repo: IFunctionRepository, id: int, data: UpdateFunctionRequestServiceDto) -> None:
        function = repo.get(id=id)
        ServiceLayerNotFoundError.when(function is None, f"Function not found. [function_id={id}]")

        function.name = data.name
        function.function_type = data.function_type
        function.validate()

        function_read = repo.get_byname(name=data.name, id_exc=id)
        ServiceLayerDuplicatedNameError.when(function_read is not None, f"This function name already exists. [function_name={data.name}]")

        repo.update(function)
        db.commit()
