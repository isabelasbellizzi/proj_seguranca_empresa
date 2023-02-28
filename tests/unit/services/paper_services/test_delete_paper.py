import pytest

from src.domain.entities import UserPermission, Feature
from src.infra.repositories.implementations import PaperRepository, UserPermissionRepository, FeatureRepository
from src.services.implementations.paper.delete_paper_service import DeletePaperService
from src.services.DTOs.user_permission import \
    ListUserPermissionServiceRequestDTO
from src.services.DTOs.feature import \
    ListFeatureServiceRequestDTO
from src.services.exceptions import ServiceLayerNotFoundError,ServiceLayerForeignKeyError
from tests.unit.services.teste_service_base import DbHandlerFake, TestServiceBase

class TestDeletePaper(TestServiceBase):

    def test_delete_paper_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db=db)
        user_per_repo = UserPermissionRepository(db=db)
        feature_repo = FeatureRepository(db=db)
        paper_id = 1

        list_user_permission = ListUserPermissionServiceRequestDTO(paper_id=paper_id)
        list_feature = ListFeatureServiceRequestDTO(paper_id=paper_id)


        mocker.patch.object(UserPermissionRepository, 'get_all', return_value=[])
        mocker.patch.object(FeatureRepository, 'get_all', return_value=[])
        mocker.patch.object(PaperRepository, 'get', return_value=paper_id)
        mocker.patch.object(PaperRepository, 'delete')
        mocker.patch.object(DbHandlerFake, 'commit')

        # Act
        DeletePaperService.execute(db=db, repo=repo, user_per_repo=user_per_repo, feature_repo=feature_repo, paper_id=paper_id)

        # Assert
        UserPermissionRepository.get_all.assert_called_once_with(data=list_user_permission)
        FeatureRepository.get_all.assert_called_once_with(data=list_feature)
        PaperRepository.get.assert_called_once_with(paper_id=paper_id)
        PaperRepository.delete.assert_called_once_with(paper_id=paper_id)
        DbHandlerFake.commit.assert_called_once()

    def test_delete_paper_has_user_permissions_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db=db)
        user_per_repo = UserPermissionRepository(db=db)
        feature_repo = FeatureRepository(db=db)
        paper_id = 1

        list_user_permission = [UserPermission(paper_id=paper_id)]

        mocker.patch.object(UserPermissionRepository, 'get_all', return_value=list_user_permission)

        # Act
        with pytest.raises(ServiceLayerForeignKeyError) as error:
            DeletePaperService.execute(db=db, repo=repo, user_per_repo=user_per_repo, feature_repo=feature_repo, paper_id=paper_id)

        # Assert
        assert str(error.value) == f"Paper has User permissions. [paper_id={paper_id}]"

    def test_delete_paper_has_feature_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db=db)
        user_per_repo = UserPermissionRepository(db=db)
        feature_repo = FeatureRepository(db=db)
        paper_id = 1

        list_feature = [Feature(paper_id=paper_id)]

        mocker.patch.object(UserPermissionRepository, 'get_all', return_value=[])
        mocker.patch.object(FeatureRepository, 'get_all', return_value=list_feature)

        # Act
        with pytest.raises(ServiceLayerForeignKeyError) as error:
            DeletePaperService.execute(db=db, repo=repo, user_per_repo=user_per_repo, feature_repo=feature_repo, paper_id=paper_id)

        # Assert
        assert str(error.value) == f"Paper has Feature. [paper_id={paper_id}]"

    def test_delete_paper_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = PaperRepository(db=db)
        user_per_repo = UserPermissionRepository(db=db)
        feature_repo = FeatureRepository(db=db)
        paper_id = 1


        mocker.patch.object(UserPermissionRepository, 'get_all', return_value=[])
        mocker.patch.object(FeatureRepository, 'get_all', return_value=[])
        mocker.patch.object(PaperRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            DeletePaperService.execute(db=db, repo=repo, user_per_repo=user_per_repo, feature_repo=feature_repo, paper_id=paper_id)

        # Assert
        PaperRepository.get.assert_called_once_with(paper_id=paper_id)
        assert str(error.value) == f"paper not found. [paper_id={paper_id}]"
