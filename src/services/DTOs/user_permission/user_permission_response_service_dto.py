from dataclasses import dataclass

from src.domain.enums.status_enum import StatusEnum


@dataclass
class UserPermissionResponseServiceDto():
    user_id: int
    paper_id: int
    user_permission_id: int
    user_email: str
    paper_name: str
    status: StatusEnum
