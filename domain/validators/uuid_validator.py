from dataclasses import dataclass
from uuid import UUID
from src.domain.exceptions.domain_validation_error import DomainValidationError

@dataclass
class UUIDValidator:
    @staticmethod
    def validate(value: UUID, field_name: str) -> None:
        DomainValidationError.when(isinstance(value, UUID) is False, f"Field {field_name} must be an UUID. [value={value}]")
