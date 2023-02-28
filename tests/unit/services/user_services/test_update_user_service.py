from uuid import uuid4

import pytest

from src.domain.entities import User
from src.infra.repositories.implementations.user_repository import \
    UserRepository
from src.services.DTOs.user.update_user_request_service_dto import \
    UpdateUserRequestServiceDto
from src.services.implementations.user.update_user_service import \
    UpdateUserService
from tests.unit.services.teste_service_base import (DbHandlerFake,
                                                    TestServiceBase)


class TestUpdateUser(TestServiceBase):

    def test_update_user_execute_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = UserRepository(db=db)
        test_id = 123
        test_email = "teste@teste.com"
        test_azure = uuid4()
        test_data = UpdateUserRequestServiceDto(azure_id=test_azure, user_email=test_email)

        mocker.patch.object(UserRepository, 'get_by_email', return_value=None)
        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            UpdateUserService.execute(db=db, repo=repo, user_id=test_id, data=test_data)

        # Assert
        UserRepository.get_by_user_id.assert_called_once_with(user_id=test_id)
        assert str(error.value) == f"User not found. [user_id={test_id}]"

    def test_update_user_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = UserRepository(db=db)
        test_id = 123
        old_test_email = "old@teste.com"
        old_test_azure = uuid4()
        new_test_email = "new@teste.com"
        new_test_azure = uuid4()
        new_test_data = UpdateUserRequestServiceDto(azure_id=new_test_azure, user_email=new_test_email)

        user_old = User(user_id=test_id, azure_id=old_test_azure, user_email=old_test_email)  # type: ignore
        user_new = User(user_id=test_id, azure_id=new_test_azure, user_email=new_test_email)  # type: ignore

        mocker.patch.object(UserRepository, 'get_by_email', return_value=None)
        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=user_old)
        mocker.patch.object(UserRepository, 'update')
        mocker.patch.object(DbHandlerFake, 'commit')

        # Act
        UpdateUserService.execute(db=db, repo=repo, user_id=test_id, data=new_test_data)

        # Assert
        UserRepository.get_by_user_id.assert_called_once_with(user_id=test_id)
        UserRepository.get_by_email.assert_called_once_with(user_email=new_test_email)
        UserRepository.update.assert_called_once_with(user_new)
        DbHandlerFake.commit.assert_called_once()
