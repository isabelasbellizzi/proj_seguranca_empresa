import pytest

from src.infra.repositories.implementations import \
    FunctionRepository, FeatureRepository
from src.services.DTOs.feature.list_feature_service_request_dto import ListFeatureServiceRequestDTO
from src.services.exceptions import \
    ServiceLayerNotFoundError, ServiceLayerForeignKeyError
from src.services.implementations.function import DeleteFunctionService
from tests.unit.services.teste_service_base import TestServiceBase, DbHandlerFake

class TestDeleteFunction (TestServiceBase):
    def test_delete_function_foreign_key_error(self, mocker):
        # Arrange
        function_id = 1234
        db = self.db_handler
        repo = FunctionRepository(db=db)
        feature_repo = FeatureRepository(db=db)

        mocker.patch.object(FunctionRepository, 'get', return_value=True)
        mocker.patch.object(FeatureRepository, 'get_all', return_value=["feature1", "feature2"])

        # Act
        with pytest.raises(ServiceLayerForeignKeyError) as error:
            DeleteFunctionService.execute(db=db, repo=repo, feature_repo=feature_repo, id=function_id)

        # Assert
        assert str(error.value) == f"Function has features. [function_id={function_id}]"

    def test_delete_function_not_found_error(self, mocker):
        # Arrange
        function_id = 1234
        db = self.db_handler
        repo = FunctionRepository(db=db)
        feature_repo = FeatureRepository(db=db)

        mocker.patch.object(FunctionRepository, 'get', return_value=None)

        # Act
        with pytest.raises(ServiceLayerNotFoundError) as error:
            DeleteFunctionService.execute(db=db, repo=repo, feature_repo=feature_repo, id=function_id)

        # Assert
        assert str(error.value) == f"Function not found. [function_id={function_id}]"

    def test_delete_execute_ok(self, mocker):
        # Arrange
        function_id = 1234
        db = self.db_handler
        repo = FunctionRepository(db=db)
        feature_repo = FeatureRepository(db=db)

        mocker.patch.object(FeatureRepository, 'get_all', return_value=[])
        mocker.patch.object(FunctionRepository, 'get', return_value=True)
        mocker.patch.object(FunctionRepository, 'delete')
        mocker.patch.object(DbHandlerFake, 'commit')

        # Act
        DeleteFunctionService.execute(db=db, repo=repo, feature_repo=feature_repo, id=function_id)

        # Assert
        FeatureRepository.get_all.assert_called_once_with(data=ListFeatureServiceRequestDTO(function_id=function_id))
        FunctionRepository.get.assert_called_once_with(id=function_id)
        FunctionRepository.delete.assert_called_once_with(id=function_id)
        DbHandlerFake.commit.assert_called_once_with()
