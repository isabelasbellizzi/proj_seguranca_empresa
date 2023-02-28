from dataclasses import dataclass

from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces import \
    IOwnerRepository
from src.services.exceptions import \
    ServiceLayerNotFoundError


@dataclass
class DeleteOwnerService:
    @staticmethod
    def execute(db: IDbHandler, repo: IOwnerRepository, owner_id: int) -> None:
        owner_read = repo.get(id=owner_id)
        ServiceLayerNotFoundError.when(owner_read is None, f"Owner not found. [owner_id={owner_id}]")

        repo.delete(id=owner_id)
        db.commit()
