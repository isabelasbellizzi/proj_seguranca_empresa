import pytest

from src.infra.repositories.implementations.paper_repository import \
    PaperRepository
from src.services.implementations.paper import GetPaperService, PaperUtils
from tests.unit.services.teste_service_base import TestServiceBase

class TestGetPaper(TestServiceBase):

    def test_get_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        paper_id = 12
        mocker.patch.object(PaperRepository, 'get', return_value=True)
        mocker.patch.object(PaperUtils, 'paper_2_paper_dto')

        # Act
        GetPaperService.execute(repo, paper_id)

        # Assert
        PaperRepository.get.assert_called_once_with(paper_id=paper_id)
        PaperUtils.paper_2_paper_dto.assassert_called_once()

    def test_get_paper_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        paper_id = 1234

        mocker.patch.object(PaperRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            GetPaperService.execute(repo, paper_id=paper_id)  # type: ignore

        # Assert
        assert str(error.value) == f"Paper not found. [paper_id={paper_id}]"
