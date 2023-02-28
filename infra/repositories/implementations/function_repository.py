from typing import List, Optional
from src.domain.entities import Function
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.ifunction_repository import \
    IFunctionRepository
from src.services.DTOs.function.list_function_service_request_dto import \
    ListFunctionServiceRequestDTO


class FunctionRepository(IFunctionRepository):
    def __init__(self, db: IDbHandler):
        self.session = db.get_session()

    def get_byname(self, name: str, id_exc: int = 0) -> Optional[Function]:
        query = self.session.query(Function).filter(Function.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(Function.name == name)

        if (id_exc != 0):
            query = query.filter(Function.function_id != id_exc)

        return query.first()

    def get(self, id: int) -> Optional[Function]:
        query = self.session.query(Function).filter(Function.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(Function.function_id == id)


        return query.first()

    def add(self, new_function: Function) -> None:
        new_function.validate()
        new_function.status = StatusEnum.ACTIVE
        new_function.function_id = None  # type: ignore
        self.session.add(new_function)
        self.session.flush()

    def delete(self, id: int) -> None:
        function = self.get(id=id)

        if function is None:
            raise Exception(f"Function not found. [function_id={id}]")

        function.status = StatusEnum.LOGICALLYDELETED
        self.session.flush()

    def update(self, function: Function) -> None:
        function.validate()
        self.session.flush()

    def get_all(self, data: ListFunctionServiceRequestDTO) -> List[Function]:
        query = self.session.query(Function).filter(Function.status != StatusEnum.LOGICALLYDELETED)

        if data.system_id is not None:
            query = query.filter(Function.system_id == data.system_id)

        if data.function_name is not None:
            query = query.filter(Function.name == data.function_name)

        if data.function_type is not None:
            query = query.filter(Function.function_type == data.function_type)

        if data.max_records > 0:
            query = query.limit(data.max_records)

        return query.all()
