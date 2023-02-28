import pytest

from src.domain.entities.function import Function
from src.domain.enums import FunctionTypeEnum
from src.infra.repositories.implementations import (FunctionRepository,
                                                    SystemRepository)
from src.services.DTOs.function.create_function_request_service_dto import \
    CreateFunctionRequestServiceDto
from src.services.implementations.function.function_utils import FunctionUtils
from src.services.implementations.function.insert_function_service import \
    InsertFunctionService
from tests.unit.services.teste_service_base import DbHandlerFake, TestServiceBase


class TestInsertFunction(TestServiceBase):
    def test_insert_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        system_repo = SystemRepository(db)
        system_id = 1234
        function_name = "nomenomenome"
        function_type = FunctionTypeEnum.EXECUTION

        create_function_dto = CreateFunctionRequestServiceDto(name=function_name, function_type=function_type, system_id=system_id)
        new_function = Function(**create_function_dto.__dict__)

        mocker.patch.object(Function, 'validate')
        mocker.patch.object(SystemRepository, 'get', return_value=True)
        mocker.patch.object(FunctionRepository, 'get_byname', return_value=None)
        mocker.patch.object(FunctionRepository, 'add')
        mocker.patch.object(DbHandlerFake, 'commit')
        mocker.patch.object(FunctionUtils, 'function_2_function_dto')

        # Act
        InsertFunctionService.execute(db=db, repo=repo, system_repo=system_repo, data=create_function_dto)

        # Assert
        Function.validate.assert_called_once_with()
        SystemRepository.get.assert_called_once_with(system_id=system_id)
        FunctionRepository.get_byname.assert_called_once_with(name=function_name)
        FunctionRepository.add.assert_called_once_with(new_function)
        DbHandlerFake.commit.assert_called_once_with()
        FunctionUtils.function_2_function_dto.assert_called_once_with(new_function)

    def test_insert_function_system_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        system_repo = SystemRepository(db)
        system_id = 1234
        function_name = "nome_duplicado"
        function_type = FunctionTypeEnum.EXECUTION

        create_function_dto = CreateFunctionRequestServiceDto(name=function_name, function_type=function_type, system_id=system_id)

        mocker.patch.object(SystemRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            InsertFunctionService.execute(db=db, repo=repo, system_repo=system_repo, data=create_function_dto)

        # Assert
        assert str(error.value) == f"System not found. [system_id={system_id}]"

    def test_insert_function_name_duplicated_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FunctionRepository(db)
        system_repo = SystemRepository(db)
        system_id = 1234
        function_name = "nome_duplicado"
        function_type = FunctionTypeEnum.EXECUTION

        create_function_dto = CreateFunctionRequestServiceDto(name=function_name, function_type=function_type, system_id=system_id)

        mocker.patch.object(SystemRepository, 'get', return_value=True)
        mocker.patch.object(FunctionRepository, 'get_byname', return_value=True)

        # Act
        with pytest.raises(Exception) as error:
            InsertFunctionService.execute(db=db, repo=repo, system_repo=system_repo, data=create_function_dto)

        # Assert
        assert str(error.value) == f"This function name already exists. [function_name={function_name}]"
