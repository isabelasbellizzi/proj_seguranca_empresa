from typing import Any
from uuid import uuid4
import pytest
from src.domain.validators.uuid_validator import UUIDValidator


class TestUUIDValidador:
    field_name = 'UUID Field'
    default_error_message = f"Field {field_name} must be an UUID."

    @pytest.mark.parametrize(
        ('uuid', 'msg_error'), (
            (None, f"{default_error_message} [value=None]"),
            ("      ", f"{default_error_message} [value=      ]"),
            ("", f"{default_error_message} [value=]"),
            ("123sdsd", f"{default_error_message} [value=123sdsd]"),
            ("32005609-d7fe-4621-8e05-01dedef8335", f"{default_error_message} [value=32005609-d7fe-4621-8e05-01dedef8335]")
        )
    )
    def test_execute_uuid_error(self, uuid: Any, msg_error: str):
        #Arrange
        uuid_test = uuid

        #act
        with pytest.raises(Exception) as error:
            UUIDValidator.validate(uuid_test, self.field_name)

        #assert
        assert str(error.value) == msg_error

    def test_execute_uuid_valido_ok(self):
        #Arrange
        uuid = uuid4()

        #act
        UUIDValidator.validate(uuid, self.field_name)

        #assert
        assert True
