from typing import Any

import pytest

from src.domain.enums.function_type_enum import FunctionTypeEnum
from src.domain.enums.status_enum import StatusEnum
from src.domain.validators.enum_validator import EnumValidator


class TestEnumValidador():
    field_name = 'enum_field'
    empty_field_default_error_msg = f"Field {field_name} must not be empty"

    @pytest.mark.parametrize(
        ('value', 'msg_error'), (
            (None, empty_field_default_error_msg),
            ("", empty_field_default_error_msg),
            (3, f"Field {field_name} must be in <enum 'StatusEnum'>. [value=3]"),
            ("string", f"Field {field_name} must be in <enum 'StatusEnum'>. [value=string]")
        )
    )
    def test_validate_error(self, value: Any, msg_error: str):
        # act
        with pytest.raises(Exception) as error:
            EnumValidator.validate(value, self.field_name, StatusEnum)

        # assert
        assert str(error.value) == msg_error

    @pytest.mark.parametrize(
        ('value'), (
            (1),
            (StatusEnum.ACTIVE),
            (FunctionTypeEnum.EXECUTION)  # deixei aqui para deixar o programador ciente que chamando outra classe de enum também funciona, desde que exista o mesmo valor na classe que estamos testando.
        )
    )
    def test_validate_ok(self, value: Any):
        # act
        EnumValidator.validate(value, self.field_name, StatusEnum)

        # assert
        assert True
