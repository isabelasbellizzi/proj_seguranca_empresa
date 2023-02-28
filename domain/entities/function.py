from dataclasses import dataclass

from src.domain.config.config_atributes import NAME_MAX_LEN
from src.domain.enums import FunctionTypeEnum, StatusEnum
from src.domain.validators import (BigIntValidator, EnumValidator,
                                   MandatoryStringValidator)


@dataclass
class Function:
    function_id: int = 0
    system_id: int = 0
    name: str = ""
    function_type: FunctionTypeEnum = FunctionTypeEnum.REGISTRATION
    status: StatusEnum = StatusEnum.ACTIVE

    def validate(self):
        MandatoryStringValidator.validate(self.name, "Name", min_length=10, max_length=NAME_MAX_LEN)
        BigIntValidator.validate(self.system_id, "system id")
        EnumValidator.validate(self.function_type, "function type", FunctionTypeEnum)
        BigIntValidator.validate(self.function_id, "function id")
        EnumValidator.validate(self.status, "status", StatusEnum)
        self.name = self.name.strip()
