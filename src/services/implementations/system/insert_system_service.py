from dataclasses import dataclass

from src.domain.entities import System
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.isystem_repository import \
    ISystemRepository
from src.services.DTOs.system import CreateSystemRequestServiceDto
from src.services.exceptions import ServiceLayerDuplicatedNameError


@dataclass
class InsertSystemService:
    @staticmethod
    def execute(repo: ISystemRepository, data: CreateSystemRequestServiceDto, db: IDbHandler) -> System:
        system_read = repo.get_byname(system_name=data.system_name)
        ServiceLayerDuplicatedNameError.when(
            system_read is not None,
            f"There is already a system with that name. [name[{data.system_name}]"
        )

        new_system = System(token_id=data.token_id, system_name=data.system_name)
        repo.add(new_system)
        db.commit()

        return new_system
