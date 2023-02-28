from uuid import uuid4

import pytest

from src.infra.repositories.implementations.user_repository import \
    UserRepository
from src.services.DTOs.user.create_user_request_service_dto import \
    CreateUserRequestServiceDto
from src.services.implementations.user.insert_user_service import \
    InsertUserService
from tests.unit.services.teste_service_base import (DbHandlerFake,
                                                    TestServiceBase)


class TestInsertUser(TestServiceBase):

    def test_insert_user_email_duplicated_error(self, mocker):
        #Arrange
        db = self.db_handler
        repo = UserRepository(db=db)
        test_azure = uuid4()
        test_email = "teste@teste.com"
        test_data = CreateUserRequestServiceDto(azure_id=test_azure, user_email=test_email)

        mocker.patch.object(UserRepository, 'get_by_email', return_value=True)

        #Act
        with pytest.raises(Exception) as Error:
            InsertUserService.execute(db=db, repo=repo, data=test_data)

        #Assert
        UserRepository.get_by_email.assert_called_once_with(user_email=test_email)
        assert str(Error.value) == f"This email was already registered. [user_email={test_email}]"


    def test_insert_execute_ok(self, mocker):
        #Arrange
        db = self.db_handler
        repo = UserRepository(db=db)
        test_email = "teste@teste.com"
        test_azure = uuid4()
        test_data = CreateUserRequestServiceDto(azure_id=test_azure, user_email=test_email)
        create_user = InsertUserService.create_user(user_email="teste@teste.com", azure_id=uuid4())

        mocker.patch.object(UserRepository, 'get_by_email', return_value=None)
        mocker.patch.object(InsertUserService, 'create_user', return_value=create_user)
        mocker.patch.object(UserRepository, 'add')
        mocker.patch.object(DbHandlerFake, 'commit')

        #Act
        obj_inserted = InsertUserService.execute(db=db, repo=repo, data=test_data)

        #Assert
        UserRepository.get_by_email.assert_called_once_with(user_email=create_user.user_email)
        UserRepository.add.assert_called_once_with(create_user)
        DbHandlerFake.commit.assert_called_once()
        assert obj_inserted.user_email == create_user.user_email
        assert obj_inserted.azure_id == create_user.azure_id
        assert obj_inserted.user_email == create_user.user_email
        assert obj_inserted.status == create_user.status
