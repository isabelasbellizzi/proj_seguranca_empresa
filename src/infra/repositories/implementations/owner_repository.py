from typing import List, Optional
from src.domain.entities import Owner
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import IOwnerRepository
from src.services.DTOs.owner import \
    ListOwnerServiceRequestDTO

class OwnerRepository(IOwnerRepository):
    def __init__(self, db: IDbHandler):
        self.session = db.get_session()

    def get(self, id: int) -> Optional[Owner]:
        query = self.session.query(Owner).filter(Owner.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(Owner.owner_id == id)
        return query.first()

    def get_all(self, data: ListOwnerServiceRequestDTO) -> List[Owner]:
        query = self.session.query(Owner).filter(Owner.status != StatusEnum.LOGICALLYDELETED)

        if data.system_id is not None:
            query = query.filter(Owner.system_id == data.system_id)

        if data.user_id is not None:
            query = query.filter(Owner.user_id == data.user_id)

        if data.status is not None:
            query = query.filter(Owner.status == data.status)

        if data.max_records > 0:
            query = query.limit(data.max_records)

        return query.all()

    def add(self, new_owner: Owner) -> None:
        new_owner.validate()
        new_owner.status = StatusEnum.ACTIVE
        new_owner.owner_id = None # type: ignore
        self.session.add(new_owner)
        self.session.flush()

    def delete(self, id: int) -> None:
        owner = self.get(id=id)

        if owner is None:
            raise Exception(f"Owner not found. [owner_id={id}]")

        owner.status = StatusEnum.LOGICALLYDELETED
        self.session.flush()

    def update(self, owner: Owner) -> None:
        owner.validate()
        self.session.flush()
