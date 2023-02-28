from dataclasses import dataclass

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.isystem_repository import \
    ISystemRepository
from src.services.DTOs.system import UpdateSystemRequestServiceDto
from src.services.exceptions.service_layer_duplicated_name_error import \
    ServiceLayerDuplicatedNameError
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError


@dataclass
class UpdateSystemService:

    @staticmethod
    def execute(db: IDbHandler, repo: ISystemRepository, system_id: int, data: UpdateSystemRequestServiceDto) -> None:
        system = repo.get(system_id=system_id)
        ServiceLayerNotFoundError.when(
            system is None,
            f"System not found. [system_id={system_id}]"
        )

        system.system_name = data.system_name
        system.token_id = data.token_id

        system_read = repo.get_byname(system_name=data.system_name, id_exc=system_id)
        ServiceLayerDuplicatedNameError.when(
            system_read is not None,
            f"There is already a system with that name. [name[{data.system_name}]"
        )

        repo.update(system)
        db.commit()
