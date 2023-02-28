from uuid import uuid4
import pytest
from src.domain.entities.system import System
from src.domain.config.config_atributes import NAME_MAX_LEN
from src.domain.validators.mandatory_string_validator import MandatoryStringValidator
from src.domain.validators.uuid_validator import UUIDValidator
from src.domain.validators.big_int_validator import BigIntValidator
from src.domain.enums.status_enum import StatusEnum
from src.domain.validators.enum_validator import EnumValidator


# O teste não funciona a não ser que os parametros de ids sejam passados como str, mesmo que gere-se um UUID
@pytest.mark.parametrize(
    ('name'), (
        ("system name  "),
        (" system name"),
        (" system name  "),
        ("system name")
    )
)
def test_validate_name_ok(name: str):
    system = System(system_name=name, system_id=11, token_id=uuid4())

    # Act
    system.validate()

    # Assert
    assert system.system_name == "system name"


def test_validate_created_without_parameters_error():
    # Arrange
    system = System(system_id=None, token_id=None)

    # Act
    with pytest.raises(Exception) as error:
        system.validate()

    # Assert
    assert str(error.value) == "system_name must not be empty"


def test_mock_validate_all_fields_ok(mocker):
    #arrange
    system = System(system_name="System Name", system_id=11, token_id=uuid4(), status=StatusEnum.ACTIVE)
    mocker.patch.object(MandatoryStringValidator, 'validate')
    mocker.patch.object(UUIDValidator, 'validate')
    mocker.patch.object(EnumValidator, 'validate')
    mocker.patch.object(BigIntValidator, 'validate')

    #act
    system.validate()

    #assert
    MandatoryStringValidator.validate.assert_called_once_with(system.system_name, "system_name", min_length=5, max_length=NAME_MAX_LEN)
    BigIntValidator.validate.assert_called_once_with(system.system_id, "system_id")
    UUIDValidator.validate.assert_called_once_with(system.token_id, "token_id")
    EnumValidator.validate.assert_called_once_with(system.status, "status", StatusEnum)


def test_non_mock_validate_all_fields_ok():
    # Arrange
    token_id = uuid4()
    system = System(system_name='Juvenal', system_id=11, token_id=token_id)

    # Act
    system.validate()

    # Assert
    assert True
