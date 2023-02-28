import pytest
from src.infra.repositories.implementations.system_repository import \
    SystemRepository
from src.services.DTOs.system import UpdateSystemRequestServiceDto
from src.services.implementations.system.insert_system_service import \
    InsertSystemService
from src.domain.enums.status_enum import StatusEnum
from tests.unit.services.teste_service_base import TestServiceBase,DbHandlerFake


class TestInsertSystem(TestServiceBase):

    def test_insert_system_duplicated_name_error(self, mocker) -> None:
        #Arrange
        name = "Tabelas Excel"
        db = self.db_handler
        repo = SystemRepository(db)
        token_id = 1234
        mocker.patch.object(SystemRepository, 'get_byname', return_value=True)
        data = UpdateSystemRequestServiceDto(token_id=token_id, system_name=name) # type: ignore

        #Act
        with pytest.raises(Exception) as error:
            InsertSystemService.execute(repo=repo, db=db, data=data) # type: ignore

        #Assert
        SystemRepository.get_byname.assert_called_once_with(system_name=name)
        assert str(error.value) == f"There is already a system with that name. [name[{name}]"

    def test_insert_system_execute_ok(self, mocker) -> None:
        #Arrange
        db = self.db_handler
        repo = SystemRepository(db)
        name = "Microsoft Word"
        token_id = 1234
        status = StatusEnum.ACTIVE
        data = UpdateSystemRequestServiceDto(token_id=token_id, system_name=name) # type: ignore
        mocker.patch.object(SystemRepository, 'get_byname', return_value=None)
        mocker.patch.object(SystemRepository, 'add')
        mocker.patch.object(DbHandlerFake, 'commit')

        #Act
        obj_inserted = InsertSystemService.execute(repo=repo, db=db, data=data) # type: ignore

        #Assert
        SystemRepository.get_byname.assert_called_once_with(system_name=name)
        DbHandlerFake.commit.assert_called_once()
        assert obj_inserted.system_name == name
        assert obj_inserted.token_id == token_id
        assert obj_inserted.status == status
