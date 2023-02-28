import pytest
from src.domain.entities.paper import Paper
from src.infra.repositories.implementations import PaperRepository, SystemRepository
from src.services.implementations.paper import InsertPaperService, PaperUtils
from src.services.DTOs.paper import CreatePaperRequestServiceDto
from tests.unit.services.teste_service_base import TestServiceBase, DbHandlerFake

class TestInsertPaper(TestServiceBase):
    def test_insert_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        system_repo = SystemRepository(db)
        system_id = 1234
        name = "testeteste"

        create_paper_dto = CreatePaperRequestServiceDto(name=name, system_id=system_id)  # type: ignore


        mocker.patch.object(SystemRepository, 'get', return_value=True)
        mocker.patch.object(PaperRepository, 'get_byname', return_value=None)
        mocker.patch.object(PaperRepository, 'add')
        mocker.patch.object(DbHandlerFake, 'commit')
        mocker.patch.object(PaperUtils, 'paper_2_paper_dto')

        # Act
        paper_inserted = InsertPaperService.execute(db=db, repo=repo, system_repo=system_repo, data=create_paper_dto)
        # Assert
        SystemRepository.get.assert_called_once_with(system_id=system_id)
        PaperRepository.get_byname.assert_called_once_with(name=name)
        PaperRepository.add.assert_called_once_with(Paper(name=name, system_id=system_id))
        DbHandlerFake.commit.assert_called_once()
        paper_inserted.system_id = system_id
        paper_inserted.name = name

    def test_insert_paper_system_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        system_repo = SystemRepository(db)
        system_id = 1234
        paper_name = "Testando"

        create_paper_dto = CreatePaperRequestServiceDto(name=paper_name, system_id=system_id)  # type: ignore
        mocker.patch.object(SystemRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            InsertPaperService.execute(db=db, repo=repo, system_repo=system_repo, data=create_paper_dto)

        # Assert
        assert str(error.value) == f"System not found. [system_id={system_id}]"


    def test_insert_paper_name_duplicated_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        system_repo = SystemRepository(db)
        system_id = 1234
        paper_name = "Testando"

        create_paper_dto = CreatePaperRequestServiceDto(name=paper_name, system_id=system_id)  # type: ignore
        mocker.patch.object(SystemRepository, 'get', return_value=True)
        mocker.patch.object(PaperRepository, 'get_byname', return_value=True)

        # Act
        with pytest.raises(Exception) as error:
            InsertPaperService.execute(db=db, repo=repo, system_repo=system_repo, data=create_paper_dto)

        # Assert
        assert str(error.value) == f"This paper name already exists. [paper_name={paper_name}]"
