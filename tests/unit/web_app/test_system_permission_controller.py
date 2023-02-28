from dotenv import load_dotenv
from fastapi.testclient import TestClient

from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.repositories.implementations import (SystemRepository,
                                                    SystemPermissionRepository)
from src.services.exceptions import ServiceLayerNotFoundError
from src.services.implementations.system_permission import ListSystemPermissionService
from src.web_app.controllers.system_permission_controller import (SystemPermissionRoute,
                                                         system_permission_route)
from src.services.DTOs.system_permission import SystemPermissionResponseServiceDTO, PermissionDTO

client = TestClient(system_permission_route)


class TesteSystemPermissionController:

    def setup_class(self) -> None:
        load_dotenv()
        self.db = DbHandler(DbConfig())
        self.repo = SystemPermissionRepository(self.db)
        self.system_repo = SystemRepository(self.db)

    def test_get_all_ok(self, mocker):
        # arrange
        system_id = 10

        response_dto = SystemPermissionResponseServiceDTO(user_id=1, user_email="email@email.com.br", permissions=[PermissionDTO(paper_id=1, paper_name="testestestesteste")])

        mocker.patch.object(SystemPermissionRoute, 'create_system_permission_repository', return_value=self.repo)
        mocker.patch.object(SystemPermissionRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(ListSystemPermissionService, "execute", return_value=[response_dto])

        # act
        response = client.get(f'/{system_id}')

        # assert
        ListSystemPermissionService.execute.assert_called_once_with(repo=self.repo, system_repo=self.system_repo, system_id=system_id)
        assert response.status_code == 200

    def test_get_all_system_not_found_error(self, mocker):
        # arrange
        system_id = 10

        mocker.patch.object(SystemPermissionRoute, 'create_system_permission_repository', return_value=self.repo)
        mocker.patch.object(SystemPermissionRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(ListSystemPermissionService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # act
        response = client.get(f'/{system_id}')

        # assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_all_generic_exception_error(self, mocker):
        # arrange
        system_id = 10

        mocker.patch.object(SystemPermissionRoute, 'create_system_permission_repository', return_value=self.repo)
        mocker.patch.object(SystemPermissionRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(ListSystemPermissionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.get(f'/{system_id}')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'
