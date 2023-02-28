import pytest

from src.domain.entities.user_permission import UserPermission
from src.infra.repositories.implementations import (PaperRepository,
                                                    UserPermissionRepository,
                                                    UserRepository)
from src.services.DTOs.user_permission import (
    CreateUserPermissionRequestServiceDto, ListUserPermissionServiceRequestDTO)
from src.services.exceptions import ServiceLayerDuplicatedObjectError
from src.services.implementations.user_permission import (
    InsertUserPermissionService, UserPermissionUtils)
from tests.unit.services.teste_service_base import (DbHandlerFake,
                                                    TestServiceBase)


class TestInsertUserPermission(TestServiceBase):

    def test_insert_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo_permission = UserPermissionRepository(db)
        paper_repo = PaperRepository(db)
        user_repo = UserRepository(db)
        user_id = 1234
        paper_id = 6

        create_user_permission_dto = CreateUserPermissionRequestServiceDto(user_id=user_id, paper_id=[paper_id])
        new_user_permission = UserPermission(user_id=user_id, paper_id=paper_id)
        list_user_permission = ListUserPermissionServiceRequestDTO(user_id=user_id, paper_id=paper_id)

        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=True)
        mocker.patch.object(PaperRepository, 'get', return_value=True)
        mocker.patch.object(UserPermissionRepository, 'get_all', return_value=[])
        mocker.patch.object(UserPermission, 'validate')
        mocker.patch.object(UserPermissionRepository, 'add')
        mocker.patch.object(DbHandlerFake, 'commit')
        mocker.patch.object(UserPermissionUtils, 'user_permission_2_user_permission_dto')

        # Act
        InsertUserPermissionService.execute(db=db, repo=repo_permission, paper_repo=paper_repo, user_repo=user_repo, data=create_user_permission_dto)

        # Assert
        UserRepository.get_by_user_id.assert_called_once_with(user_id=user_id)
        PaperRepository.get.assert_called_once_with(paper_id=paper_id)
        UserPermissionRepository.get_all.assert_called_once_with(data=list_user_permission)
        UserPermission.validate.assert_called_once_with()
        UserPermissionRepository.add.assert_called_once_with(new_user_permission)
        DbHandlerFake.commit.assert_called_once()
        UserPermissionUtils.user_permission_2_user_permission_dto(new_user_permission)


    def test_insert_user_permission_user_id_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo_permission = UserPermissionRepository(db)
        paper_repo = PaperRepository(db)
        user_repo = UserRepository(db)
        user_id = 1234
        paper_id = 6

        create_user_permission_dto = CreateUserPermissionRequestServiceDto(user_id=user_id, paper_id=[paper_id])  # type: ignore
        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            InsertUserPermissionService.execute(db=db, repo=repo_permission, paper_repo=paper_repo, user_repo=user_repo, data=create_user_permission_dto)

        # Assert
        assert str(error.value) == f"user_id not found. [user_id={create_user_permission_dto.user_id}]"

    def test_insert_user_permission_paper_id_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo_permission = UserPermissionRepository(db)
        paper_repo = PaperRepository(db)
        user_repo = UserRepository(db)
        user_id = 1234
        paper_id = 6

        create_user_permission_dto = CreateUserPermissionRequestServiceDto(user_id=user_id, paper_id=[paper_id])  # type: ignore
        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=True)
        mocker.patch.object(PaperRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            InsertUserPermissionService.execute(db=db, repo=repo_permission, paper_repo=paper_repo, user_repo=user_repo, data=create_user_permission_dto)


        # Assert
        assert str(error.value) == f"paper_id not found. [paper_id={paper_id}]"

    def test_insert_user_permission_already_exists_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo_permission = UserPermissionRepository(db)
        paper_repo = PaperRepository(db)
        user_repo = UserRepository(db)
        user_id = 1234
        paper_id = 6
        user_permission_id = 1

        create_user_permission_dto = CreateUserPermissionRequestServiceDto(user_id=user_id, paper_id=[paper_id])  # type: ignore
        list_user_permission = [UserPermission(user_permission_id=user_permission_id, user_id=user_id, paper_id=paper_id)]

        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=True)
        mocker.patch.object(PaperRepository, 'get', return_value=True)
        mocker.patch.object(UserPermissionRepository, 'get_all', return_value=list_user_permission)

        # Act
        with pytest.raises(ServiceLayerDuplicatedObjectError) as error:
            InsertUserPermissionService.execute(db=db, repo=repo_permission, paper_repo=paper_repo, user_repo=user_repo, data=create_user_permission_dto)

        # Assert
        assert str(error.value) == f"User [user_id={user_id}] already has permissions [paper_ids: {[paper_id]}]."
