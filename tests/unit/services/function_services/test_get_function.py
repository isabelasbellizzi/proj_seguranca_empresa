import pytest

from src.domain.entities import Function
from src.infra.repositories.implementations.function_repository import \
    FunctionRepository
from src.services.implementations.function.function_utils import FunctionUtils
from src.services.implementations.function.get_function_service import \
    GetFunctionService
from tests.unit.services.teste_service_base import TestServiceBase


class TestGetFunction(TestServiceBase):
    def test_get_function_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        function_id = 1234

        mocker.patch.object(FunctionRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            GetFunctionService.execute(repo, id=function_id)

        # Assert
        assert str(error.value) == f"Function not found. [function_id={function_id}]"

    def test_get_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        function_id = 1234

        function = Function(function_id=function_id, system_id=1, name="fhjsdfhsdjkfhdjk")

        mocker.patch.object(FunctionRepository, 'get', return_value=function)
        mocker.patch.object(FunctionUtils, 'function_2_function_dto')

        # Act
        GetFunctionService.execute(repo, id=function_id)

        # Assert
        FunctionRepository.get.assert_called_once_with(id=function_id)
        FunctionUtils.function_2_function_dto.assert_called_once_with(function)