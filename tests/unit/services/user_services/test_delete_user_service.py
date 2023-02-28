import pytest

from src.infra.repositories.implementations.user_permission_repository import \
    UserPermissionRepository
from src.infra.repositories.implementations.user_repository import \
    UserRepository
from src.infra.repositories.implementations.owner_repository import \
    OwnerRepository
from src.services.DTOs.user_permission import \
    ListUserPermissionServiceRequestDTO
from src.services.implementations.user.delete_user_service import \
    DeleteUserService
from tests.unit.services.teste_service_base import (DbHandlerFake,
                                                    TestServiceBase)
from src.services.DTOs.owner import ListOwnerServiceRequestDTO

class TestDeleteUser(TestServiceBase):

    def test_delete_user_execute_not_found_error(self, mocker):
        #Arrange
        test_id = 1234
        db = self.db_handler
        repo = UserRepository(db=db)
        up_repo = UserPermissionRepository(db=db)
        owner_repo = OwnerRepository(db=db)
        

        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=None)

        #Act
        with pytest.raises(Exception) as error:
            DeleteUserService.execute(db=db, repo=repo, up_repo=up_repo, user_id=test_id, owner_repo=owner_repo)

        #Assert
        UserRepository.get_by_user_id.assert_called_once_with(user_id=test_id)
        assert str(error.value) == f"User not found. [user_id={test_id}]"


    def test_delete_user_with_permissions_error(self, mocker):
        #Arrange
        test_id = 1234
        db = self.db_handler
        repo = UserRepository(db=db)
        up_repo = UserPermissionRepository(db=db)
        list_user_permission_request_dto = ListUserPermissionServiceRequestDTO(user_id=test_id)
        owner_repo = OwnerRepository(db=db)

        mocker.patch.object(UserRepository, 'get_by_user_id')
        mocker.patch.object(UserPermissionRepository, 'get_all', return_value=[list_user_permission_request_dto])

        #Act
        with pytest.raises(Exception) as error:
            DeleteUserService.execute(db=db, repo=repo, up_repo=up_repo, user_id=test_id, owner_repo=owner_repo)

        #Assert
        UserPermissionRepository.get_all.assert_called_once_with(data=list_user_permission_request_dto)
        assert str(error.value) == f"User has permissions. [user_id={test_id}]"
        
    def test_delete_owner_user_error(self, mocker):
        #Arrange
        test_id = 1234
        db = self.db_handler
        repo = UserRepository(db=db)
        owner_repo = OwnerRepository(db=db)
        up_repo = UserPermissionRepository(db=db)
        list_owner_request_dto = ListOwnerServiceRequestDTO(user_id=test_id)

        mocker.patch.object(UserRepository, 'get_by_user_id')
        mocker.patch.object(UserPermissionRepository, 'get_all')
        mocker.patch.object(OwnerRepository, 'get_all', return_value=[list_owner_request_dto])

        #Act
        with pytest.raises(Exception) as error:
            DeleteUserService.execute(db=db, repo=repo, up_repo=up_repo, user_id=test_id, owner_repo=owner_repo)

        #Assert
        OwnerRepository.get_all.assert_called_once_with(data=list_owner_request_dto)
        assert str(error.value) == f"User is an owner [user_id={test_id}]"


    def test_delete_user_execute_ok(self, mocker):
        #Arrange
        test_id = 1234
        db = self.db_handler
        repo = UserRepository(db=db)
        owner_repo = OwnerRepository(db=db)
        up_repo = UserPermissionRepository(db=db)
        
        
        mocker.patch.object(UserRepository, 'get_by_user_id')
        mocker.patch.object(UserPermissionRepository, 'get_all', return_value=[])
        mocker.patch.object(OwnerRepository, 'get_all', return_value=[])
        mocker.patch.object(UserRepository, 'delete')
        mocker.patch.object(DbHandlerFake, 'commit')

        #Act
        DeleteUserService.execute(db=db, repo=repo, up_repo=up_repo, user_id=test_id, owner_repo=owner_repo)

        #Assert
        UserRepository.get_by_user_id.assert_called_once_with(user_id=test_id)
        UserRepository.delete.assert_called_once_with(user_id=test_id)
        DbHandlerFake.commit.assert_called_once()
