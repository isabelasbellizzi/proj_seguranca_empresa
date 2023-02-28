import pytest

from src.infra.repositories.implementations.user_permission_repository import \
    UserPermissionRepository
from src.services.implementations.user_permission import (
    GetUserPermissionService, UserPermissionUtils)
from tests.unit.services.teste_service_base import TestServiceBase


class TestGetUserPermission(TestServiceBase):
    
    def test_get_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = UserPermissionRepository(db=db)
        user_permission_id = 12
        mocker.patch.object(UserPermissionRepository, 'get', return_value=True)
        mocker.patch.object(UserPermissionUtils, 'user_permission_2_user_permission_dto')

        # Act
        GetUserPermissionService.execute(repo, user_permission_id)

        # Assert
        UserPermissionRepository.get.assert_called_once_with(user_permission_id=user_permission_id)
        UserPermissionUtils.user_permission_2_user_permission_dto.assassert_called_once()

    def test_get_user_permission_not_found_error(self, mocker):
        # Arrange
        user_permission_id = 10
        db = self.db_handler
        repo = UserPermissionRepository(db=db)
        mocker.patch.object(UserPermissionRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            GetUserPermissionService.execute(repo=repo, user_permission_id=user_permission_id)

        # Assert
        UserPermissionRepository.get.assert_called_once_with(user_permission_id=user_permission_id)
        assert str(error.value) == f"User permission id not found. [user permission id={user_permission_id}]"
