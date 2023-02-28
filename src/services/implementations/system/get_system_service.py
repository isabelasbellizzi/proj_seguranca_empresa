from dataclasses import dataclass
from typing import Optional
from src.domain.entities import System
from src.infra.repositories.interfaces.isystem_repository import ISystemRepository
from src.services.exceptions import ServiceLayerNotFoundError

@dataclass
class GetSystemService:

    @staticmethod
    def execute(repo: ISystemRepository, system_id: int) -> Optional[System]:
        system = repo.get(system_id=system_id)
        ServiceLayerNotFoundError.when(system is None, f"System not found. [system_id={system_id}]")

        return system
