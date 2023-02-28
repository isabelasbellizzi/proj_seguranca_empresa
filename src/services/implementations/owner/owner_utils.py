from dataclasses import dataclass

from src.domain.entities.owner import Owner
from src.services.DTOs.owner import OwnerResponseServiceDto


@dataclass
class OwnerUtils:
    @staticmethod
    def owner_2_owner_dto(ori: Owner) -> OwnerResponseServiceDto:
        return OwnerResponseServiceDto(
            system_id=ori.system_id,
            user_id=ori.user_id,
            owner_id=ori.owner_id,
            user_email=ori.user.user_email,
            system_name=ori.system.system_name,
            status=ori.status
        )
