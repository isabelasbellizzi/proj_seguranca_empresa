from dataclasses import dataclass, field
from typing import List

from .permission_dto import PermissionDTO


@dataclass
class SystemPermissionResponseServiceDTO:
    user_id: int
    user_email: str
    permissions: List[PermissionDTO] = field(default_factory=list)
