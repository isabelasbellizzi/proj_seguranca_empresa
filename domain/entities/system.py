from dataclasses import dataclass
from uuid import UUID, uuid4

from src.domain.config.config_atributes import NAME_MAX_LEN
from src.domain.enums.status_enum import StatusEnum
from src.domain.validators.enum_validator import EnumValidator
from src.domain.validators.mandatory_string_validator import \
    MandatoryStringValidator
from src.domain.validators import UUIDValidator, BigIntValidator


@dataclass
class System:
    system_id: int = 0
    token_id: UUID = uuid4()
    system_name: str = ""
    status: StatusEnum = StatusEnum.ACTIVE

    def validate(self) -> None:
        self.system_name = self.system_name or ""
        MandatoryStringValidator.validate(self.system_name,'system_name', min_length=5, max_length=NAME_MAX_LEN)
        self.system_name = self.system_name.strip()

        BigIntValidator.validate(self.system_id, 'system_id')
        UUIDValidator.validate(self.token_id, 'token_id')
        EnumValidator.validate(self.status, 'status', StatusEnum)
