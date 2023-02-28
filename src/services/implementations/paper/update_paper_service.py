from dataclasses import dataclass
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import IPaperRepository
from src.services.exceptions import ServiceLayerNotFoundError,ServiceLayerDuplicatedNameError
from src.services.DTOs.paper import UpdatePaperRequestServiceDto

@dataclass
class UpdatePaperService:

    @staticmethod
    def execute(db: IDbHandler, repo: IPaperRepository, paper_id: int, data: UpdatePaperRequestServiceDto) -> None:
        paper = repo.get(paper_id=paper_id)
        ServiceLayerNotFoundError.when(paper is None, f"Paper not found. [paper_id={paper_id}]")

        paper.name = data.name
        paper.validate()

        paper_read = repo.get_byname(name=data.name, id_exc=paper_id)
        ServiceLayerDuplicatedNameError.when(paper_read is not None, f"This paper name already exists. [paper_name={data.name}]")

        repo.update(paper)
        db.commit()
