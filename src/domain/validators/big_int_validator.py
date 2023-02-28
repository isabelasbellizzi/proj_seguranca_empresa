from dataclasses import dataclass
from src.domain.exceptions.domain_validation_error import DomainValidationError

@dataclass
class BigIntValidator:
    @staticmethod
    def validate(value, field_name: str) -> None:
        DomainValidationError.when(not isinstance(value, int), f"Field {field_name} must be an BigInt. [value={value}]")
        DomainValidationError.when(value < 0, f"Field {field_name} must be a positive BigInt. [value={value}]")
