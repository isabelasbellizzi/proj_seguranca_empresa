import pytest

from src.domain.entities import Feature
from src.infra.repositories.implementations import (FeatureRepository,
                                                    FunctionRepository,
                                                    PaperRepository)
from src.services.DTOs.feature import CreateFeatureRequestServiceDto, ListFeatureServiceRequestDTO
from src.services.exceptions import ServiceLayerNotFoundError, ServiceLayerDuplicatedObjectError
from src.services.implementations.feature import (FeatureUtils,
                                                  InsertFeatureService)
from tests.unit.services.teste_service_base import DbHandlerFake, TestServiceBase


class TestInsertFeature(TestServiceBase):
    def test_insert_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FeatureRepository(db)
        paper_repo = PaperRepository(db)
        function_repo = FunctionRepository(db)
        create = True
        read = True
        update = True
        delete = True
        paper_id = 1234
        function_id = 5678

        create_feature_dto = CreateFeatureRequestServiceDto(create=create, read=read, update=update, delete=delete, paper_id=paper_id, function_id=function_id)
        new_feature = Feature(paper_id=paper_id, function_id=function_id, create=create, read=read, update=update, delete=delete)
        list_feature_request_dto = ListFeatureServiceRequestDTO(paper_id=paper_id, function_id=function_id)

        mocker.patch.object(Feature, 'validate')
        mocker.patch.object(FunctionRepository, 'get', return_value=True)
        mocker.patch.object(PaperRepository, 'get', return_value=True)
        mocker.patch.object(FeatureRepository, 'get_all', return_value=[])
        mocker.patch.object(FeatureRepository, 'add')
        mocker.patch.object(DbHandlerFake, 'commit')
        mocker.patch.object(FeatureUtils, 'feature_2_feature_dto')

        # Act
        InsertFeatureService.execute(db=db, repo=repo, function_repo=function_repo, paper_repo=paper_repo, data=create_feature_dto)

        # Assert
        Feature.validate.assert_called_once_with()
        FunctionRepository.get.assert_called_once_with(id=function_id)
        PaperRepository.get.assert_called_once_with(paper_id=paper_id)
        FeatureRepository.get_all.assert_called_once_with(data=list_feature_request_dto)
        FeatureRepository.add.assert_called_once_with(new_feature)
        DbHandlerFake.commit.assert_called_once_with()
        FeatureUtils.feature_2_feature_dto.assert_called_once_with(new_feature)

    def test_insert_feature_function_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FeatureRepository(db)
        paper_repo = PaperRepository(db)
        function_repo = FunctionRepository(db)
        create = True
        read = True
        update = True
        delete = True
        paper_id = 1234
        function_id = 5678

        create_feature_dto = CreateFeatureRequestServiceDto(create=create, read=read, update=update, delete=delete, paper_id=paper_id, function_id=function_id)

        mocker.patch.object(FunctionRepository, 'get', return_value=None)

        # Act
        with pytest.raises(ServiceLayerNotFoundError) as error:
            InsertFeatureService.execute(db=db, repo=repo, function_repo=function_repo, paper_repo=paper_repo, data=create_feature_dto)

        # Assert
        assert str(error.value) == f"Function not found. [function_id={function_id}]"

    def test_insert_feature_paper_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FeatureRepository(db)
        paper_repo = PaperRepository(db)
        function_repo = FunctionRepository(db)
        create = True
        read = True
        update = True
        delete = True
        paper_id = 1234
        function_id = 5678

        create_feature_dto = CreateFeatureRequestServiceDto(create=create, read=read, update=update, delete=delete, paper_id=paper_id, function_id=function_id)

        mocker.patch.object(FunctionRepository, 'get', return_value=True)
        mocker.patch.object(PaperRepository, 'get', return_value=None)

        # Act
        with pytest.raises(ServiceLayerNotFoundError) as error:
            InsertFeatureService.execute(db=db, repo=repo, function_repo=function_repo, paper_repo=paper_repo, data=create_feature_dto)

        # Assert
        assert str(error.value) == f"Paper not found. [paper_id={paper_id}]"

    def test_insert_feature_duplicated_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = FeatureRepository(db)
        paper_repo = PaperRepository(db)
        function_repo = FunctionRepository(db)
        create = True
        read = True
        update = True
        delete = True
        paper_id = 1234
        function_id = 5678
        feature_id = 4321

        create_feature_dto = CreateFeatureRequestServiceDto(create=create, read=read, update=update, delete=delete, paper_id=paper_id, function_id=function_id)
        duplicated_feature_list = [Feature(feature_id=feature_id, paper_id=paper_id, function_id=function_id, create=create, read=read, update=update, delete=delete)]

        mocker.patch.object(FunctionRepository, 'get', return_value=True)
        mocker.patch.object(PaperRepository, 'get', return_value=True)
        mocker.patch.object(FeatureRepository, 'get_all', return_value=duplicated_feature_list)

        # Act
        with pytest.raises(ServiceLayerDuplicatedObjectError) as error:
            InsertFeatureService.execute(db=db, repo=repo, function_repo=function_repo, paper_repo=paper_repo, data=create_feature_dto)

        # Assert
        assert str(error.value) == f"A feature with this paper_id and this function_id already exists. [feature_id={feature_id}]"
