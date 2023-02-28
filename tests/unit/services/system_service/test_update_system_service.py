from uuid import uuid4
import pytest
from src.domain.entities.system import System
from src.infra.repositories.implementations.system_repository import \
    SystemRepository
from src.services.DTOs.system import UpdateSystemRequestServiceDto
from src.services.implementations.system.update_system_service import \
    UpdateSystemService
from tests.unit.services.teste_service_base import TestServiceBase,DbHandlerFake


class TestUpdateSystem(TestServiceBase):

    name = "Tabelas Excel"
    token_id = uuid4()
    data = UpdateSystemRequestServiceDto(token_id=token_id, system_name=name)


    def test_update_system_duplicated_name_error(self, mocker) -> None:
        #Arrange
        system_id = 11
        db = self.db_handler
        repo = SystemRepository(db)
        mocker.patch.object(SystemRepository, 'get_byname', return_value=False)
        mocker.patch.object(SystemRepository, 'get')

        #Act
        with pytest.raises(Exception) as error:
            UpdateSystemService.execute(
                db=db,
                repo=repo,
                data=self.data,
                system_id=system_id
            )

        #Assert
        SystemRepository.get_byname.assert_called_once_with(system_name=self.data.system_name, id_exc=system_id)
        assert str(error.value) == f"There is already a system with that name. [name[{self.data.system_name}]"

    def test_update_system_not_found_error(self, mocker) -> None:
        #Arrange
        system_id = 11
        db = self.db_handler
        repo = SystemRepository(db)
        mocker.patch.object(SystemRepository, 'get_byname', return_value=None)
        mocker.patch.object(SystemRepository, 'get', return_value=None)

        #Act
        with pytest.raises(Exception) as error:
            UpdateSystemService.execute(
                db=db,
                repo=repo,
                data=self.data,
                system_id=system_id
            )

        #Assert
        SystemRepository.get.assert_called_once_with(system_id=system_id)
        assert str(error.value) == f"System not found. [system_id={system_id}]"


    def test_update_system_execute_ok(self, mocker) -> None:
        #Arrange
        system_id = 11
        db = self.db_handler
        repo = SystemRepository(db)

        system_not_updated = System(system_name='Slides PowerPoint', system_id=system_id, token_id=uuid4())
        system_updated = System(system_name=self.name, system_id=system_id, token_id=self.token_id)

        mocker.patch.object(SystemRepository, 'get_byname', return_value=None)
        mocker.patch.object(SystemRepository, 'get', return_value=system_not_updated)
        mocker.patch.object(SystemRepository, 'update')
        mocker.patch.object(DbHandlerFake, 'commit')

        #Act
        UpdateSystemService.execute(
            db=db,
            repo=repo,
            data=self.data,
            system_id=system_id
        )

        #Assert
        SystemRepository.get_byname.assert_called_once_with(system_name=self.name, id_exc=system_id)
        SystemRepository.get.assert_called_once_with(system_id=system_id)
        SystemRepository.update.assert_called_once_with(system_updated)
        DbHandlerFake.commit.assert_called_once()
