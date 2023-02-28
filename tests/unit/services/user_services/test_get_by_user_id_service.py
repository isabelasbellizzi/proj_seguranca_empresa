from uuid import uuid4

import pytest

from src.infra.repositories.implementations.user_repository import \
    UserRepository
from src.services.implementations.user.get_user_by_id_service import \
    GetUserByIdService
from tests.unit.services.teste_service_base import TestServiceBase


class TestGetUser(TestServiceBase):

    def test_get_system_not_found_error(self, mocker):
        #Arrange
        test_id = 123
        db = self.db_handler
        repo = UserRepository(db=db)
        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=None)

        #Act
        with pytest.raises(Exception) as error:
            GetUserByIdService.execute(repo=repo, user_id=test_id)  # type: ignore

        #Assert
        UserRepository.get_by_user_id.assert_called_once_with(user_id=test_id)
        assert str(error.value) == f"User not found. [user_id={test_id}]"


    def test_get_user_ok(self, mocker):
        # Arrange
        test_id = 123
        db = self.db_handler
        repo = UserRepository(db=db)
        mocker.patch.object(UserRepository, 'get_by_user_id')

        # Act
        GetUserByIdService.execute(repo, user_id=test_id)  # type: ignore

        # Assert
        UserRepository.get_by_user_id.assert_called_once_with(user_id=test_id)
