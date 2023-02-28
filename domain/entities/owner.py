from dataclasses import dataclass
from src.domain.enums import StatusEnum
from src.domain.validators import (BigIntValidator, EnumValidator)


@dataclass
class Owner:
    owner_id: int = 0
    system_id: int = 0
    user_id: int = 0
    status: StatusEnum = StatusEnum.ACTIVE

    def validate(self) -> None:

        BigIntValidator.validate(self.owner_id, 'owner_id')
        BigIntValidator.validate(self.system_id, 'system_id')
        BigIntValidator.validate(self.user_id, 'user_id')
        EnumValidator.validate(self.status, 'status', StatusEnum)
