from dataclasses import dataclass
from src.domain.enums.status_enum import StatusEnum
from src.domain.validators import (BigIntValidator,
                                   EnumValidator)


@dataclass
class Feature:
    feature_id: int = 0
    paper_id: int = 0
    function_id: int = 0
    status: StatusEnum = StatusEnum.ACTIVE
    create: bool = False
    read: bool = False
    update: bool = False
    delete: bool = False


    def validate(self) -> None:
        EnumValidator.validate(
            self.status,
            'status',
            StatusEnum
        )

        BigIntValidator.validate(
            self.feature_id,
            'feature_id'
        )

        BigIntValidator.validate(
            self.paper_id,
            'paper_id'
        )

        BigIntValidator.validate(
            self.function_id,
            'function_id'
        )
