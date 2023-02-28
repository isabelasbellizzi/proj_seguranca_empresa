from dataclasses import dataclass
from uuid import UUID, uuid4

from src.domain.enums.status_enum import StatusEnum
from src.domain.validators import EmailValidator, EnumValidator, UUIDValidator, BigIntValidator


@dataclass
class User:
    user_id: int = 0
    azure_id: UUID = uuid4()
    user_email: str = ""
    status: StatusEnum = StatusEnum.ACTIVE

    def validate(self):
        BigIntValidator.validate(self.user_id, "user_id")
        UUIDValidator.validate(self.azure_id, "azure_id")
        EmailValidator.validate(self.user_email)
        self.user_email = self.user_email.strip()

        EnumValidator.validate(self.status, "status", StatusEnum)
