from dataclasses import dataclass

from src.domain.exceptions.domain_validation_error import DomainValidationError


@dataclass
class EnumValidator:
    @staticmethod
    def validate(value, field_name: str, enum_class) -> None:
        empty_field_default_error_msg: str = f"Field {field_name} must not be empty"
        DomainValidationError.when(value is None, empty_field_default_error_msg)
        DomainValidationError.when(value == "", empty_field_default_error_msg)
        DomainValidationError.when(value not in list(enum_class), f"Field {field_name} must be in {enum_class}. [value={value}]")
