from typing import List
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from src.domain.enums.status_enum import StatusEnum

from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.repositories.implementations import (PaperRepository,
                                                    UserPermissionRepository,
                                                    UserRepository)
from src.services.DTOs.user_permission import \
    CreateUserPermissionRequestServiceDto, UserPermissionResponseServiceDto, ListUserPermissionServiceRequestDTO
from src.services.exceptions import ServiceLayerNotFoundError, ServiceLayerDuplicatedObjectError
from src.services.implementations.user_permission import (
    DeleteUserPermissionService, GetUserPermissionService,
    InsertUserPermissionService, ListUserPermissionService)
from src.web_app.controllers.user_permission_controller import (
    UserPermissionRoute, user_permission_route)

client = TestClient(user_permission_route)


class TesteUserPermissionController:

    def setup_class(self) -> None:
        load_dotenv()
        self.db = DbHandler(DbConfig())
        self.repo = UserPermissionRepository(self.db)
        self.paper_repo = PaperRepository(self.db)
        self.user_repo = UserRepository(self.db)

    def test_get_ok(self, mocker):
        # arrange
        user_permission_id = 10
        user_permission_return = UserPermissionResponseServiceDto(user_id=1234, paper_id=1, user_permission_id=2, user_email="teste@teste.com", paper_name="Teste", status=StatusEnum.ACTIVE)

        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(GetUserPermissionService, "execute", return_value=user_permission_return)

        # act
        response = client.get(f'/{user_permission_id}')

        # assert
        GetUserPermissionService.execute.assert_called_once_with(repo=self.repo, user_permission_id=user_permission_id)
        assert response.status_code == 200

    def test_get_not_found_error(self, mocker):
        # arrange
        user_permission_id = 10

        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(GetUserPermissionService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # act
        response = client.get(f'/{user_permission_id}')

        # assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_generic_exception_error(self, mocker):
        # arrange
        user_permission_id = 10

        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(GetUserPermissionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.get(f'/{user_permission_id}')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'


    def test_get_all_parameters_ok(self, mocker):
        # arrange
        max_records = 3
        user_id = 1234
        paper_id = 12345
        list_user_permission_dto = ListUserPermissionServiceRequestDTO(max_records=max_records, user_id=user_id, paper_id=paper_id)

        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(ListUserPermissionService, "execute", return_value=[])

        # act
        response = client.get(f'/?max_records={max_records}&user_id={user_id}&paper_id={paper_id}')

        # assert
        ListUserPermissionService.execute.assert_called_once_with(repo=self.repo, data=list_user_permission_dto)
        assert response.status_code == 200

    def test_get_all_default_values_ok(self, mocker):
        # arrange
        user_permission_return = UserPermissionResponseServiceDto(user_id=1234, paper_id=1, user_permission_id=2, user_email="teste@teste.com", paper_name="Teste", status=StatusEnum.ACTIVE)
        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(ListUserPermissionService, "execute", return_value=[user_permission_return])
        list_user_permission_dto = ListUserPermissionServiceRequestDTO(max_records=0, user_id=None, paper_id=None)

        # act
        response = client.get('/')

        # assert
        ListUserPermissionService.execute.assert_called_once_with(repo=self.repo, data=list_user_permission_dto)
        assert response.status_code == 200

    def test_get_all_generic_exception_error(self, mocker):
        # arrange

        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(ListUserPermissionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.get('/')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_delete_ok(self, mocker):
        # arrange
        user_permission_id = 10

        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(DeleteUserPermissionService, "execute")

        # act
        response = client.delete(f'/{user_permission_id}')

        # assert
        DeleteUserPermissionService.execute.assert_called_once_with(db=self.db, repo=self.repo, user_permission_id=user_permission_id)
        assert response.status_code == 204

    def test_delete_not_found_error(self, mocker):
        # arrange
        user_permission_id = 10

        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(DeleteUserPermissionService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # act
        response = client.delete(f'/{user_permission_id}')

        # assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_delete_generic_exception_error(self, mocker):
        # arrange
        user_permission_id = 10

        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(DeleteUserPermissionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.delete(f'/{user_permission_id}')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_insert_ok(self, mocker):
        # arrange
        user_id = 1234
        paper_id = [123]
        create_user_permission_dto = CreateUserPermissionRequestServiceDto(user_id=user_id, paper_id=paper_id)
        user_permission_return = UserPermissionResponseServiceDto(user_id=user_id, paper_id=123, user_permission_id=1, user_email="teste@teste.com", paper_name="teste", status=StatusEnum.ACTIVE)

        mocker.patch.object(UserPermissionRoute, 'create_paper_repository', return_value=self.paper_repo)
        mocker.patch.object(UserPermissionRoute, 'create_user_repository', return_value=self.user_repo)
        mocker.patch.object(UserPermissionRoute, 'create_user_permission_repository', return_value=self.repo)
        mocker.patch.object(InsertUserPermissionService, "execute", return_value=[user_permission_return])
        
        # act
        response = client.post('/', json={"user_id": user_id, "paper_id": paper_id})

        # assert
        InsertUserPermissionService.execute.assert_called_once_with(db=self.db, repo=self.repo, paper_repo=self.paper_repo, user_repo=self.user_repo, data=create_user_permission_dto)
        assert response.status_code == 201

    # ServiceLayerDuplicatedNameError
    def test_insert_not_found_error(self, mocker):
        # arrange
        user_id = 1234
        paper_id = [123, 321, 000]

        mocker.patch.object(InsertUserPermissionService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # act
        response = client.post('/', json={"user_id": user_id, "paper_id": paper_id})

        # assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_insert_duplicated_object_error(self, mocker):
        # arrange
        user_id = 1234
        paper_id = [12345, 54321, 00000]

        mocker.patch.object(InsertUserPermissionService, "execute", side_effect=ServiceLayerDuplicatedObjectError('Exception mocked'))

        # act
        response = client.post('/', json={"user_id": user_id, "paper_id": paper_id})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    # generic exception error
    def test_insert_generic_exception_error(self, mocker):
        # arrange
        user_id = 1234
        paper_id = [12345, 54321, 00000]

        mocker.patch.object(InsertUserPermissionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.post('/', json={"user_id": user_id, "paper_id": paper_id})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'
