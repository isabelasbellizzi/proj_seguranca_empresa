import pytest

from src.infra.repositories.implementations.user_permission_repository import \
    UserPermissionRepository
from src.services.implementations.user_permission.delete_user_permission_service import \
    DeleteUserPermissionService
from tests.unit.services.teste_service_base import (DbHandlerFake,
                                                    TestServiceBase)


class TestDeleteUserPermission(TestServiceBase):

    def test_delete_user_permission_execute_ok(self, mocker):
        # Arrange
        user_permission_id = 1
        db = self.db_handler
        repo = UserPermissionRepository(db=db)
        mocker.patch.object(UserPermissionRepository, 'get', return_value=True)
        mocker.patch.object(UserPermissionRepository, 'delete')
        mocker.patch.object(DbHandlerFake, 'commit')

        # Act
        DeleteUserPermissionService.execute(db=db, repo=repo, user_permission_id=user_permission_id)

        # Assert
        UserPermissionRepository.get.assert_called_once_with(user_permission_id=user_permission_id)
        UserPermissionRepository.delete.assert_called_once_with(user_permission_id=user_permission_id)
        DbHandlerFake.commit.assert_called_once()

    def test_delete_user_permission_not_found_error(self, mocker):
        # Arrange
        user_permission_id = 10
        db = self.db_handler
        repo = UserPermissionRepository(db=db)
        mocker.patch.object(UserPermissionRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            DeleteUserPermissionService.execute(db=db, repo=repo, user_permission_id=user_permission_id)

        # Assert
        UserPermissionRepository.get.assert_called_once_with(user_permission_id=user_permission_id)
        assert str(error.value) == f"User permission id not found. [user permission id={user_permission_id}]"
