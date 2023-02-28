from src.infra.repositories.implementations.paper_repository import PaperRepository
from src.services.implementations.paper.list_paper_service import ListPaperService
from src.services.DTOs.paper.list_paper_service_request_dto import \
    ListPaperServiceRequestDTO
from src.domain.enums import StatusEnum
from tests.unit.services.teste_service_base import TestServiceBase


class TestListPaper(TestServiceBase):
    def test_list_execute_parameters_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db)
        mocker.patch.object(PaperRepository, 'get_all')
        max_records = 5
        system_id = 1234
        paper_name = "paper_name"
        paper_status = StatusEnum.ACTIVE

        paper_list = ListPaperServiceRequestDTO(max_records, system_id, paper_name, paper_status)
        mocker.patch.object(PaperRepository, 'get_all')

        # Act
        ListPaperService.execute(repo, data=paper_list)

        # Assert
        PaperRepository.get_all.assert_called_once_with(data=paper_list)
