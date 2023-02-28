import pytest

from src.infra.repositories.implementations.features_repository import FeatureRepository
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError
from src.services.implementations.feature import DeleteFeatureService
from tests.unit.services.teste_service_base import DbHandlerFake, TestServiceBase


class TestDeleteFeature (TestServiceBase):
    def test_delete_feature_not_found_error(self, mocker):
        # Arrange
        feature_id = 1234
        db = self.db_handler
        repo = FeatureRepository(db=db)
        mocker.patch.object(FeatureRepository, 'get', return_value=None)

        # Act
        with pytest.raises(ServiceLayerNotFoundError) as error:
            DeleteFeatureService.execute(db=db, repo=repo, feature_id=feature_id)

        # Assert
        assert str(error.value) == f"Feature not found. [feature_id={feature_id}]"

    def test_delete_execute_ok(self, mocker):
        # Arrange
        feature_id = 1234
        db = self.db_handler
        repo = FeatureRepository(db=db)

        mocker.patch.object(FeatureRepository, 'get', return_value=True)
        mocker.patch.object(FeatureRepository, 'delete')
        mocker.patch.object(DbHandlerFake, 'commit')

        # Act
        DeleteFeatureService.execute(db=db, repo=repo, feature_id=feature_id)

        # Assert
        FeatureRepository.get.assert_called_once_with(id=feature_id)
        FeatureRepository.delete.assert_called_once_with(id=feature_id)
        DbHandlerFake.commit.assert_called_once_with()
