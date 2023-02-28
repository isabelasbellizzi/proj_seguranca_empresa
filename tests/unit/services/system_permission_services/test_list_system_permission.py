import pytest

from tests.unit.services.teste_service_base import TestServiceBase
from src.services.implementations.system_permission import ListSystemPermissionService
from src.infra.repositories.implementations import SystemPermissionRepository, SystemRepository


class TestListSystemPermission(TestServiceBase):
    def test_execute_system_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = SystemPermissionRepository(db=db)
        system_repo = SystemRepository(db=db)
        system_id = 1

        mocker.patch.object(SystemRepository, "get", return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            ListSystemPermissionService.execute(repo=repo, system_repo=system_repo, system_id=system_id)

        # Assert
        assert str(error.value) == f"System not found. [system_id={system_id}]"

    def test_execute_parameters_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = SystemPermissionRepository(db=db)
        system_repo = SystemRepository(db=db)
        system_id = 1

        mocker.patch.object(SystemRepository, "get")
        mocker.patch.object(SystemPermissionRepository, "get_all")

        # Act

        ListSystemPermissionService.execute(repo=repo, system_repo=system_repo, system_id=system_id)

        # Assert
        SystemRepository.get.assert_called_once_with(system_id=system_id)
        SystemPermissionRepository.get_all.assert_called_once_with(system_id=system_id)
        # testar o dto?
