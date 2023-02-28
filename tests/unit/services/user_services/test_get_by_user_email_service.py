import pytest

from src.infra.repositories.implementations.user_repository import \
    UserRepository
from src.services.implementations.user.get_by_user_email import \
    GetUserByEmailService
from tests.unit.services.teste_service_base import TestServiceBase


class TestGetUserByName(TestServiceBase):
    def test_get_user_by_email_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = UserRepository(db=db)
        test_email = "teste"

        mocker.patch.object(UserRepository, 'get_by_email', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            GetUserByEmailService.execute(repo=repo, user_email=test_email)

        # Assert
        assert str(error.value) == f"User not found. [user_email={test_email}]"


    def test_get_by_user_email_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = UserRepository(db=db)
        test_email = "teste@teste.com"
        mocker.patch.object(UserRepository, 'get_by_email')

        # Act
        GetUserByEmailService.execute(repo, user_email=test_email)

        # Assert
        UserRepository.get_by_email.assert_called_once_with(user_email=test_email)
