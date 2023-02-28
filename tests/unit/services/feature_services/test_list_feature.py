from src.infra.repositories.implementations import FeatureRepository
from src.services.DTOs.feature import ListFeatureServiceRequestDTO
from src.services.implementations.feature import ListFeatureService, FeatureUtils
from tests.unit.services.teste_service_base import TestServiceBase
from src.domain.entities import Feature


class TestListFeature(TestServiceBase):
    def test_list_execute_parameters_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FeatureRepository(db)
        max_records = 5
        paper_id = 1234
        function_id = 5678
        list_feature_request_dto = ListFeatureServiceRequestDTO(max_records=max_records, paper_id=paper_id, function_id=function_id)

        feature = Feature(feature_id=1234, paper_id=1, function_id=1)

        mocker.patch.object(FeatureRepository, 'get_all', return_value=[feature])
        mocker.patch.object(FeatureUtils, 'feature_2_feature_dto')

        # Act
        ListFeatureService.execute(repo=repo, data=list_feature_request_dto)

        # Assert
        FeatureRepository.get_all.assert_called_once_with(data=list_feature_request_dto)
        FeatureUtils.feature_2_feature_dto.assert_called_once_with(feature)
