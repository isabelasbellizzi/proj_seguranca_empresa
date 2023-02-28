from uuid import uuid4
from src.infra.repositories.implementations.system_repository import \
    SystemRepository
from src.services.implementations.system.list_system_service import \
    ListSystemService
from src.services.DTOs.system import UpdateSystemRequestServiceDto
from tests.unit.services.teste_service_base import TestServiceBase

class TestListSystem(TestServiceBase):

    def test_list_system_execute_parameters_ok(self, mocker):
        #Arrange
        db = self.db_handler
        name = "Tabelas Excel"
        token_id = uuid4()
        data = UpdateSystemRequestServiceDto(
            token_id=token_id,
            system_name=name
        )
        mocker.patch.object(SystemRepository, 'get_all')

        #Act
        ListSystemService.execute(
            SystemRepository(db),
            data=data #type:ignore
        )

        #Assert
        SystemRepository.get_all.assert_called_once_with(
            data=UpdateSystemRequestServiceDto(
                token_id=token_id,
                system_name='Tabelas Excel'
            )
        )
