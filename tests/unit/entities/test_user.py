from uuid import UUID, uuid4

import pytest

from src.domain.entities.user import User
from src.domain.enums.status_enum import StatusEnum
from src.domain.validators import EmailValidator, EnumValidator, UUIDValidator, BigIntValidator


class TestUser:
    def test_mock_validate_all_fields_ok(self, mocker):
        # Arrange
        user = User(user_id=1234, azure_id=uuid4(), status=StatusEnum.ACTIVE)
        mocker.patch.object(EmailValidator, 'validate')
        mocker.patch.object(UUIDValidator, 'validate')
        mocker.patch.object(EnumValidator, 'validate')
        mocker.patch.object(BigIntValidator, 'validate')

        # Act
        user.validate()

        # Assert
        EmailValidator.validate.assert_called_once_with(user.user_email)
        UUIDValidator.validate.assert_called_once_with(user.azure_id, "azure_id")
        EnumValidator.validate.assert_called_once_with(user.status, "status", StatusEnum)
        BigIntValidator.validate.assert_called_once_with(user.user_id, "user_id")


    def test_user_created_without_parameters_error(self):
        # Arrange
        user = User(user_id=None, azure_id=None)

        # Act
        with pytest.raises(Exception) as erro:
            user.validate()

        # Assert
        assert str(erro.value) == f"Field user_id must be an BigInt. [value={user.user_id}]"


    @pytest.mark.parametrize(

        ('id', 'msg_erro'), (
            (None, "Field user_id must be an BigInt. [value=None]"),
            ("", "Field user_id must be an BigInt. [value=]"),
            ("12345", "Field user_id must be an BigInt. [value=12345]"),))
    def test_validate_user_id_error(self, id: int, msg_erro: str):
        # Arrange
        user = User(user_id=id, azure_id=uuid4(), user_email="teste@teste.com")

        # Act
        with pytest.raises(Exception) as erro:
            user.validate()

        # Assert
        assert str(erro.value) == msg_erro


    @pytest.mark.parametrize(

        ('id', 'msg_erro'), (
            (None, "Field azure_id must be an UUID. [value=None]"),
            ("", "Field azure_id must be an UUID. [value=]"),
            ("12345", "Field azure_id must be an UUID. [value=12345]")))
    def test_validate_azure_id_error(self, id: UUID, msg_erro: str):
        user = User(user_id=1234, azure_id=id, user_email="teste@teste.com")


        with pytest.raises(Exception) as erro:
            user.validate()

        assert str(erro.value) == msg_erro

    def test_validate_all_fields_ok(self):
        # Arrange
        email = "teste@teste.com"
        id_user = 1234
        id_azure = uuid4()
        user = User(user_email=email, user_id=id_user, azure_id=id_azure)

        # Act
        user.validate()

        # Assert
        assert True
