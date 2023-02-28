import pytest
from src.infra.repositories.implementations.paper_repository import PaperRepository
from src.services.implementations.paper.get_byname_paper_service import GetByNamePaperService
from tests.unit.services.teste_service_base import TestServiceBase

class TestGetByNamePaper(TestServiceBase):

    def test_get_byname_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        paper_name = "abc"
        mocker.patch.object(PaperRepository, 'get_byname', return_value=True)

        # Act
        GetByNamePaperService.execute(repo, paper_name=paper_name)

        # Assert
        PaperRepository.get_byname.assert_called_once_with(name=paper_name)

    def test_get_byname_paper_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        paper_name = "abc"

        mocker.patch.object(PaperRepository, 'get_byname', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            GetByNamePaperService.execute(repo, paper_name=paper_name)

        # Assert
        PaperRepository.get_byname.assert_called_once_with(name=paper_name)
        assert str(error.value) == f"Paper not found. [paper_name={paper_name}]"
