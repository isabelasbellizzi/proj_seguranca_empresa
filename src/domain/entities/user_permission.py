from dataclasses import dataclass
from src.domain.enums.status_enum import StatusEnum
from src.domain.validators import (BigIntValidator, EnumValidator)


@dataclass
class UserPermission:
    user_permission_id: int = 0
    user_id: int = 0
    paper_id: int = 0
    status: StatusEnum = StatusEnum.ACTIVE

    def validate(self):
        BigIntValidator.validate(self.user_permission_id, "user_permission_id")

        BigIntValidator.validate(self.user_id, "user_id")

        BigIntValidator.validate(self.paper_id, "paper_id")

        EnumValidator.validate(self.status, "status", StatusEnum)
