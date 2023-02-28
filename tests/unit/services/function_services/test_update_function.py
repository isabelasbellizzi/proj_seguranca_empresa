import pytest

from src.domain.entities.function import Function
from src.domain.enums import FunctionTypeEnum
from src.infra.repositories.implementations import FunctionRepository
from src.services.DTOs.function.update_function_request_service_dto import \
    UpdateFunctionRequestServiceDto
from src.services.implementations.function.update_function_service import \
    UpdateFunctionService
from tests.unit.services.teste_service_base import DbHandlerFake, TestServiceBase


class TestUpdateFunction(TestServiceBase):
    def test_update_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        function_id = 1234
        new_function_name = "nomenomenome"
        new_function_type = FunctionTypeEnum.EXECUTION

        update_function_dto = UpdateFunctionRequestServiceDto(name=new_function_name, function_type=new_function_type)

        function_not_updated = Function(function_id=function_id, name="oldnomenomenome", function_type=FunctionTypeEnum.REGISTRATION)
        function_updated = Function(function_id=function_id, name=new_function_name, function_type=new_function_type)

        mocker.patch.object(Function, 'validate')
        mocker.patch.object(FunctionRepository, 'get', return_value=function_not_updated)
        mocker.patch.object(FunctionRepository, 'get_byname', return_value=None)
        mocker.patch.object(FunctionRepository, 'update')
        mocker.patch.object(DbHandlerFake, 'commit')

        # Act
        UpdateFunctionService.execute(db=db, repo=repo, id=function_id, data=update_function_dto)

        # Assert
        FunctionRepository.get.assert_called_once_with(id=function_id)
        Function.validate.assert_called_once_with()
        FunctionRepository.get_byname.assert_called_once_with(name=new_function_name, id_exc=function_id)
        FunctionRepository.update.assert_called_once_with(function_updated)
        db.commit.assert_called_once()

    def test_update_function_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        function_id = 1234
        new_function_name = "nomenomenome"
        new_function_type = FunctionTypeEnum.EXECUTION

        update_function_dto = UpdateFunctionRequestServiceDto(name=new_function_name, function_type=new_function_type)

        mocker.patch.object(FunctionRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            UpdateFunctionService.execute(db=db, repo=repo, id=function_id, data=update_function_dto)

        # Assert
        assert str(error.value) == f"Function not found. [function_id={function_id}]"

    def test_update_function_duplicated_name_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        function_id = 1234
        new_function_name = "nomenomenome"
        new_function_type = FunctionTypeEnum.EXECUTION

        update_function_dto = UpdateFunctionRequestServiceDto(name=new_function_name, function_type=new_function_type)
        function_not_updated = Function(function_id=function_id, name="oldnomenomenome", function_type=FunctionTypeEnum.REGISTRATION)

        mocker.patch.object(FunctionRepository, 'get', return_value=function_not_updated)
        mocker.patch.object(FunctionRepository, 'get_byname', return_value=True)

        # Act
        with pytest.raises(Exception) as error:
            UpdateFunctionService.execute(db=db, repo=repo, id=function_id, data=update_function_dto)

        # Assert
        assert str(error.value) == f"This function name already exists. [function_name={update_function_dto.name}]"
