from typing import List, Optional
from src.domain.entities import System
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.isystem_repository import ISystemRepository
from src.services.DTOs.system import ListSystemServiceRequestDTO

class SystemRepository(ISystemRepository):
    def __init__(self, db: IDbHandler):
        self.session = db.get_session()

    def get_byname(self, system_name: str, id_exc: int = 0) -> Optional[System]:
        query = self.session.query(System).filter(System.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(System.system_name == system_name)

        if (id_exc != 0):
            query = query.filter(System.system_id != id_exc)

        return query.first()

    def get(self, system_id: int) -> Optional[System]:
        query = self.session.query(System).filter(System.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(System.system_id == system_id)
        return query.first()

    def get_all(self, data: ListSystemServiceRequestDTO) -> List[System]:
        query = self.session.query(System).filter(System.status != StatusEnum.LOGICALLYDELETED)

        if data.system_name is not None:
            query = query.filter(System.system_name == data.system_name)

        if data.system_status is not None:
            query = query.filter(System.status == data.system_status)

        if data.max_records > 0:
            query = query.limit(data.max_records)

        return query.all()

    def add(self, new: System) -> None:
        new.validate()
        new.system_id = None # type: ignore
        new.status = StatusEnum.ACTIVE
        self.session.add(new)
        self.session.flush()

    def delete(self, system_id: int) -> None:
        obj = self.get(system_id=system_id)

        if not obj:
            raise Exception(f"System not found. [system_id={system_id}]")

        obj.status = StatusEnum.LOGICALLYDELETED
        self.session.flush()

    def update(self, obj: System) -> None:
        obj.validate()
        self.session.flush()
