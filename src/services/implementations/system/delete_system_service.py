from dataclasses import dataclass
from typing import List
from src.domain.entities import Function, Paper, Owner

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import \
    ISystemRepository, IFunctionRepository, IPaperRepository, IOwnerRepository
from src.services.exceptions import \
    ServiceLayerNotFoundError, ServiceLayerForeignKeyError
from src.services.DTOs.function import ListFunctionServiceRequestDTO
from src.services.DTOs.paper import ListPaperServiceRequestDTO
from src.services.DTOs.owner import ListOwnerServiceRequestDTO



@dataclass
class DeleteSystemService:

    @staticmethod
    def execute(db: IDbHandler, repo: ISystemRepository, function_repo: IFunctionRepository, paper_repo: IPaperRepository, owner_repo: IOwnerRepository, system_id: int):
        owner_read: List[Owner] = owner_repo.get_all(data=ListOwnerServiceRequestDTO(system_id=system_id))
        ServiceLayerForeignKeyError.when(len(owner_read) > 0, f"System has owners. [system_id={system_id}]")

        functions_read: List[Function] = function_repo.get_all(data=ListFunctionServiceRequestDTO(system_id=system_id))
        ServiceLayerForeignKeyError.when(len(functions_read) > 0, f"System has functions. [id={system_id}]")

        paper_read: List[Paper] = paper_repo.get_all(data=ListPaperServiceRequestDTO(system_id=system_id))
        ServiceLayerForeignKeyError.when(len(paper_read) > 0, f"System has papers. [id={system_id}]")

        system_read = repo.get(system_id=system_id)
        ServiceLayerNotFoundError.when(system_read is None, f"System not found. [id={system_id}]")

        repo.delete(system_id=system_id)
        db.commit()
