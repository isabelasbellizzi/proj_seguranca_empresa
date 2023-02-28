import pytest

from src.domain.config.config_atributes import NAME_MAX_LEN
from src.domain.entities.function import Function
from src.domain.enums.function_type_enum import FunctionTypeEnum
from src.domain.enums.status_enum import StatusEnum
from src.domain.validators.big_int_validator import BigIntValidator
from src.domain.validators.enum_validator import EnumValidator
from src.domain.validators.mandatory_string_validator import \
    MandatoryStringValidator


class TestFunction:
    def test_validate_mandatorystr_validator_parameters_ok(self, mocker):
        # arrange
        function = Function(name="nome", system_id=1234, status=StatusEnum.LOGICALLYDELETED)

        mocker.patch.object(MandatoryStringValidator, 'validate')
        mocker.patch.object(BigIntValidator, 'validate')
        mocker.patch.object(EnumValidator, 'validate')

        calls_bigint_validator = [
            mocker.call(function.system_id, "system id"),
            mocker.call(function.function_id, "function id")
        ]
        calls_enum_validator = [
            mocker.call(function.function_type, "function type", FunctionTypeEnum),
            mocker.call(function.status, "status", StatusEnum)
        ]

        # act
        function.validate()

        # assert
        MandatoryStringValidator.validate.assert_called_once_with(function.name, "Name", min_length=10, max_length=NAME_MAX_LEN)
        BigIntValidator.validate.assert_has_calls(calls_bigint_validator)
        EnumValidator.validate.assert_has_calls(calls_enum_validator)

    @pytest.mark.parametrize(
        ('name'), (
            ("function name  "),
            (" function name"),
            (" function name  "),
            ("function name")
        )
    )
    def test_validate_name_strip_ok(self, name: str):
        function = Function(name=name, function_id=1, system_id=1234)

        # Act
        function.validate()

        # Assert
        assert function.name == "function name"
