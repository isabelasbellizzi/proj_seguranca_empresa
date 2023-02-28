import re
from dataclasses import dataclass

from src.domain.exceptions.domain_validation_error import DomainValidationError


@dataclass
class EmailValidator:
    @staticmethod
    def validate(value: str) -> None:
        DomainValidationError.when(value is None, "invalid E-mail. [value=]")
        DomainValidationError.when(not isinstance(value, str), f"invalid Email.[value={value}] must be a string",)

        value = value.strip()
        email_regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        email_validator = email_regex.findall(value)

        DomainValidationError.when(value not in email_validator, f"invalid E-mail. [value={value}]")
