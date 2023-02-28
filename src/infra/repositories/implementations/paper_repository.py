from typing import List, Optional
from src.domain.entities import Paper
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.ipaper_repository import IPaperRepository
from src.services.DTOs.paper.list_paper_service_request_dto import \
    ListPaperServiceRequestDTO

class PaperRepository(IPaperRepository):
    def __init__(self, db: IDbHandler):
        self.session = db.get_session()

    def get_byname(self, name: str, id_exc: int = 0) -> Optional[Paper]:
        query = self.session.query(Paper).filter(Paper.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(Paper.name == name)

        if (id_exc != 0):
            query = query.filter(Paper.paper_id != id_exc)

        return query.first()

    def get(self, paper_id: int) -> Optional[Paper]:
        query = self.session.query(Paper).filter(Paper.status != StatusEnum.LOGICALLYDELETED)
        query = query.filter(Paper.paper_id == paper_id)
        return query.first()

    def get_all(self, data: ListPaperServiceRequestDTO) -> List[Paper]:
        query = self.session.query(Paper).filter(Paper.status != StatusEnum.LOGICALLYDELETED)

        if data.system_id is not None:
            query = query.filter(Paper.system_id == data.system_id)

        if data.paper_name is not None:
            query = query.filter(Paper.name == data.paper_name)

        if data.paper_status is not None:
            query = query.filter(Paper.status == data.paper_status)

        if data.max_records > 0:
            query = query.limit(data.max_records)

        return query.all()

    def add(self, new_paper: Paper) -> None:
        new_paper.validate()
        new_paper.status = StatusEnum.ACTIVE
        new_paper.paper_id = None # type: ignore
        self.session.add(new_paper)
        self.session.flush()

    def delete(self, paper_id: int) -> None:
        paper = self.get(paper_id=paper_id)

        if paper is None:
            raise Exception(f"Paper not found. [paper_id={paper_id}]")

        paper.status = StatusEnum.LOGICALLYDELETED
        self.session.flush()

    def update(self, paper: Paper) -> None:
        paper.validate()
        self.session.flush()
