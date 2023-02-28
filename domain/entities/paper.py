from dataclasses import dataclass
from src.domain.config.config_atributes import NAME_MAX_LEN
from src.domain.enums import StatusEnum
from src.domain.validators import (BigIntValidator, EnumValidator,
                                   MandatoryStringValidator)


@dataclass
class Paper:
    paper_id: int = 0
    system_id: int = 0
    name: str = ""
    status: StatusEnum = StatusEnum.ACTIVE

    def validate(self) -> None:

        MandatoryStringValidator.validate(self.name, 'name', min_length=5, max_length=NAME_MAX_LEN)
        self.name = self.name.strip()
        BigIntValidator.validate(self.paper_id, 'paper_id')
        BigIntValidator.validate(self.system_id, 'system_id')
        EnumValidator.validate(self.status, 'status', StatusEnum)
