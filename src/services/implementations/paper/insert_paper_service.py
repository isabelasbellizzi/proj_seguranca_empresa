from dataclasses import dataclass
from src.domain.entities import Paper
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import IPaperRepository,ISystemRepository
from src.services.exceptions import ServiceLayerDuplicatedNameError,ServiceLayerNotFoundError
from src.services.DTOs.paper import CreatePaperRequestServiceDto
from src.services.implementations.paper.paper_utils import PaperUtils

@dataclass
class InsertPaperService:

    @staticmethod
    def execute(db: IDbHandler, repo: IPaperRepository, system_repo: ISystemRepository, data: CreatePaperRequestServiceDto):
        new_paper = Paper(**data.__dict__)
        new_paper.validate()

        system_read = system_repo.get(system_id=new_paper.system_id)
        ServiceLayerNotFoundError.when(system_read is None, f"System not found. [system_id={new_paper.system_id}]")

        paper_read = repo.get_byname(name=new_paper.name)
        ServiceLayerDuplicatedNameError.when(paper_read is not None, f"This paper name already exists. [paper_name={new_paper.name}]")

        repo.add(new_paper)
        db.commit()

        return PaperUtils().paper_2_paper_dto(new_paper)
