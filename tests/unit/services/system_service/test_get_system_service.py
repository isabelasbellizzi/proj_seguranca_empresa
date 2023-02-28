import pytest
from src.infra.repositories.implementations.system_repository import SystemRepository
from src.services.implementations.system.get_system_service import GetSystemService
from tests.unit.services.teste_service_base import TestServiceBase

class TestGetSystem(TestServiceBase):

    def test_get_system_not_found_error(self, mocker):
        #Arrange
        db = self.db_handler
        system_id = "123"
        repo = SystemRepository(db)
        mocker.patch.object(SystemRepository, 'get', return_value=None)

        #Act
        with pytest.raises(Exception) as error:
            GetSystemService.execute(repo=repo, system_id=system_id)

        #Assert
        SystemRepository.get.assert_called_once_with(system_id=system_id)
        assert str(error.value) == f"System not found. [system_id={system_id}]"


    def test_get_system_ok(self, mocker):
        #Arrange
        db = self.db_handler
        system_id = 1234
        repo = SystemRepository(db)
        mocker.patch.object(SystemRepository, 'get', return_value=True)

        #Act
        GetSystemService.execute(repo=repo, system_id=system_id)

        #Assert
        SystemRepository.get.assert_called_once_with(system_id=system_id)
