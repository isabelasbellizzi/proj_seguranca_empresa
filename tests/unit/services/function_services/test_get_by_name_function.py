import pytest

from src.infra.repositories.implementations.function_repository import \
    FunctionRepository
from src.services.implementations.function.get_by_name_function_service import \
    GetByNameFunctionService
from tests.unit.services.teste_service_base import TestServiceBase


class TestGetByNameFunction(TestServiceBase):
    def test_get_byname_function_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        function_name = "abc"

        mocker.patch.object(FunctionRepository, 'get_byname', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            GetByNameFunctionService.execute(repo, name=function_name)

        # Assert
        assert str(error.value) == f"Function not found. [function_name={function_name}]"

    def test_get_byname_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        function_name = "abc"

        mocker.patch.object(FunctionRepository, 'get_byname', return_value=True)

        # Act
        GetByNameFunctionService.execute(repo, name=function_name)

        # Assert
        FunctionRepository.get_byname.assert_called_once_with(name=function_name)
