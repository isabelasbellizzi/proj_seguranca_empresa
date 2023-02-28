import pytest
from src.domain.entities.paper import Paper
from src.infra.repositories.implementations import PaperRepository
from src.services.implementations.paper.update_paper_service import UpdatePaperService
from src.services.DTOs.paper import UpdatePaperRequestServiceDto
from tests.unit.services.teste_service_base import TestServiceBase,DbHandlerFake


class TestUpdatePaper(TestServiceBase):

    def test_update_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        paper_id = 1234
        new_paper_name = "Testando"

        paper_updated_dto = UpdatePaperRequestServiceDto(name=new_paper_name)
        paper_not_updated = Paper(paper_id=paper_id, system_id=1234, name=new_paper_name)
        paper_updated = Paper(paper_id=paper_id, system_id=paper_not_updated.system_id, name=new_paper_name)


        mocker.patch.object(PaperRepository, 'get', return_value=paper_not_updated)
        mocker.patch.object(PaperRepository, 'get_byname', return_value=None)
        mocker.patch.object(PaperRepository, 'update')
        mocker.patch.object(DbHandlerFake, 'commit')

        # Act
        UpdatePaperService.execute(db=db, repo=repo, paper_id=paper_id, data=paper_updated_dto)

        # Assert
        PaperRepository.get.assert_called_once_with(paper_id=paper_id)
        PaperRepository.get_byname.assert_called_once_with(name=new_paper_name, id_exc=paper_id)
        PaperRepository.update.assert_called_once_with(paper_updated)
        DbHandlerFake.commit.assert_called_once()

    def test_update_paper_duplicated_name_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        paper_id = 1234
        new_paper_name = "Testando"

        paper_updated_dto = UpdatePaperRequestServiceDto(name=new_paper_name)
        paper_not_updated = Paper(paper_id=paper_id, system_id=1234, name="oldnomenomenome")

        mocker.patch.object(PaperRepository, 'get', return_value=paper_not_updated)
        mocker.patch.object(PaperRepository, 'get_byname', return_value=True)

        # Act
        with pytest.raises(Exception) as error:
            UpdatePaperService.execute(db=db, repo=repo, paper_id=paper_id, data=paper_updated_dto)

        # Assert
        assert str(error.value) == f"This paper name already exists. [paper_name={paper_updated_dto.name}]"

    def test_update_paper_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        paper_id = 123
        new_paper_name = "Testandooo"

        paper_updated_dto = UpdatePaperRequestServiceDto(name=new_paper_name)

        mocker.patch.object(PaperRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            UpdatePaperService.execute(db=db, repo=repo, paper_id=paper_id, data=paper_updated_dto)

        # Assert

        assert str(error.value) == f"Paper not found. [paper_id={paper_id}]"
