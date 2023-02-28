import pytest

from src.infra.repositories.implementations.features_repository import FeatureRepository
from src.services.implementations.feature import (FeatureUtils,
                                                  GetFeatureService)
from src.domain.entities import Feature
from tests.unit.services.teste_service_base import TestServiceBase


class TestGetFeature(TestServiceBase):
    def test_get_feature_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FeatureRepository(db)
        feature_id = 1234

        mocker.patch.object(FeatureRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            GetFeatureService.execute(repo, id=feature_id)

        # Assert
        assert str(error.value) == f"Feature not found. [feature_id={feature_id}]"

    def test_get_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FeatureRepository(db)
        feature_id = 1234

        feature = Feature(feature_id=feature_id, paper_id=1, function_id=1)

        mocker.patch.object(FeatureRepository, 'get', return_value=feature)
        mocker.patch.object(FeatureUtils, 'feature_2_feature_dto')

        # Act
        GetFeatureService.execute(repo=repo, id=feature_id)

        # Assert
        FeatureRepository.get.assert_called_once_with(id=feature_id)
        FeatureUtils.feature_2_feature_dto.assert_called_once_with(feature)
