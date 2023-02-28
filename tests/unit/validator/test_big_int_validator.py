from typing import Any
import pytest
from src.domain.validators.big_int_validator import BigIntValidator


class TestBigIntValidator():
    field_name = 'BigInt Field'

    default_error_message = f"Field {field_name} must be an BigInt."


    @pytest.mark.parametrize(
        ('big_int', 'msg_error'), (
            (None, f"{default_error_message} [value=None]"),
            ("", f"{default_error_message} [value=""]"),
            ('123sdsd', f"{default_error_message} [value=123sdsd]")
        )
    )
    def test_execute_big_int_error(self, big_int: Any, msg_error: str):
        #Arrange
        big_int_test = big_int

        #act
        with pytest.raises(Exception) as error:
            BigIntValidator.validate(big_int_test, self.field_name)

        #assert
        assert str(error.value) == msg_error

    def test_execute_big_int_valid_ok(self):
        #Arrange
        big_int = 16465465464646464646464646464646464646466464646464646464646464646464

        #act
        BigIntValidator.validate(big_int, self.field_name)

        #assert
        assert True

    def test_execute_big_int_negative_error(self):
        #Arrange
        big_int = -16465465464646464646464646464646464646466464646464646464646464646464
        field_name = "BigInt Field"

        #act
        with pytest.raises(Exception) as error:
            BigIntValidator.validate(big_int, self.field_name)

        #assert
        assert str(error.value) == f'Field {field_name} must be a positive BigInt. [value={big_int}]'
