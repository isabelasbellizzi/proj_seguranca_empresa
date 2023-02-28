import pytest

from src.domain.entities import Feature
from src.infra.repositories.implementations import FeatureRepository
from src.services.DTOs.feature import UpdateFeatureRequestServiceDto
from src.services.implementations.feature.update_feature_service import \
    UpdateFeatureService
from tests.unit.services.teste_service_base import DbHandlerFake, TestServiceBase


class TestUpdateFunction(TestServiceBase):
    def test_update_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FeatureRepository(db)
        feature_id = 1234
        paper_id = 5678
        function_id = 4321

        update_feature_dto = UpdateFeatureRequestServiceDto(create=True, read=True, update=True, delete=True)

        feature_not_updated = Feature(feature_id=feature_id, paper_id=paper_id, function_id=function_id)
        feature_updated = Feature(feature_id=feature_id, paper_id=paper_id, function_id=function_id, create=True, read=True, update=True, delete=True)

        mocker.patch.object(Feature, 'validate')
        mocker.patch.object(FeatureRepository, 'get', return_value=feature_not_updated)
        mocker.patch.object(FeatureRepository, 'update')
        mocker.patch.object(DbHandlerFake, 'commit')

        # Act
        UpdateFeatureService.execute(db=db, repo=repo, feature_id=feature_id, data=update_feature_dto)

        # Assert
        Feature.validate.assert_called_once_with()
        FeatureRepository.get.assert_called_once_with(id=feature_id)
        FeatureRepository.update.assert_called_once_with(feature_updated)
        db.commit.assert_called_once()

    def test_update_feature_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FeatureRepository(db)
        feature_id = 1234

        update_feature_dto = UpdateFeatureRequestServiceDto(create=True, read=True, update=True, delete=True)

        mocker.patch.object(FeatureRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            UpdateFeatureService.execute(db=db, repo=repo, feature_id=feature_id, data=update_feature_dto)

        # Assert
        assert str(error.value) == f"Feature not found. [feature_id={feature_id}]"
