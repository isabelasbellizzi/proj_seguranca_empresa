from src.infra.repositories.implementations.function_repository import \
    FunctionRepository
from src.services.implementations.function.list_function_service import \
    ListFunctionService, FunctionUtils
from src.services.DTOs.function import \
    ListFunctionServiceRequestDTO, FunctionResponseServiceDto
from src.domain.enums import FunctionTypeEnum, StatusEnum
from tests.unit.services.teste_service_base import TestServiceBase


class TestListFunction(TestServiceBase):
    def test_list_execute_parameters_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        max_records = 5
        system_id = 1234
        function_name = "function_name"
        function_type = FunctionTypeEnum.EXECUTION

        data = ListFunctionServiceRequestDTO(max_records=max_records, system_id=system_id, function_name=function_name, function_type=function_type)
        response_dto = FunctionResponseServiceDto(name=function_name, function_type=function_type, system_id=system_id, function_id=1234, name_system="idjgfsghfkdjghf", status=StatusEnum.ACTIVE)

        mocker.patch.object(FunctionRepository, 'get_all', return_value=[response_dto])
        mocker.patch.object(FunctionUtils, 'function_2_function_dto')

        # Act
        ListFunctionService.execute(repo, data=data)

        # Assert
        FunctionRepository.get_all.assert_called_once_with(data=data)
        FunctionUtils.function_2_function_dto.assert_called_once_with(response_dto)
