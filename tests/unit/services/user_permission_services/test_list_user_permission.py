from src.infra.repositories.implementations.user_permission_repository import \
    UserPermissionRepository
from src.services.DTOs.user_permission import \
    ListUserPermissionServiceRequestDTO
from src.services.implementations.user_permission import \
    ListUserPermissionService
from tests.unit.services.teste_service_base import TestServiceBase


class TestListUserPermission(TestServiceBase):

    def test_list_execute_parameters_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = UserPermissionRepository(db)
        mocker.patch.object(UserPermissionRepository, 'get_all')
        max_records = 5
        user_id = 1234
        paper_id = 3

        list_user_permission = ListUserPermissionServiceRequestDTO(user_id=user_id, paper_id=paper_id)

        # Act
        user_permission_list = ListUserPermissionService.execute(repo, list_user_permission)

        # Assert
        UserPermissionRepository.get_all.assert_called_once_with(data=list_user_permission)
        assert len(user_permission_list) <= max_records
        for user_permission in user_permission_list:
            assert user_permission.user_id == user_id
            assert user_permission.user_id == user_id
