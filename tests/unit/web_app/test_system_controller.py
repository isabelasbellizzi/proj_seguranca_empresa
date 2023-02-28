from uuid import UUID, uuid4

from dotenv import load_dotenv
from fastapi.testclient import TestClient

from src.domain.entities.system import System
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.repositories.implementations import \
    SystemRepository, FunctionRepository, PaperRepository, OwnerRepository
from src.services.DTOs.system import SystemResponseServiceDto, ListSystemServiceRequestDTO, CreateSystemRequestServiceDto, UpdateSystemRequestServiceDto
from src.services.exceptions import \
    ServiceLayerNotFoundError, ServiceLayerDuplicatedNameError, ServiceLayerForeignKeyError
from src.services.implementations.system import (DeleteSystemService,
                                                 GetSystemService,
                                                 InsertSystemService,
                                                 ListSystemService,
                                                 UpdateSystemService)
from src.web_app.controllers.system_controller import SystemRoute, system_route

client = TestClient(system_route)


class TesteSystemController:

    def setup_class(self) -> None:
        load_dotenv()
        self.db = DbHandler(DbConfig())  # pylint: disable=attribute-defined-outside-init
        self.repo = SystemRepository(self.db)  # pylint: disable=attribute-defined-outside-init
        self.repo_function = FunctionRepository(self.db) # pylint: disable=attribute-defined-outside-init
        self.repo_paper = PaperRepository(self.db) # pylint: disable=attribute-defined-outside-init
        self.repo_owner = OwnerRepository(self.db)

    def test_get_not_found_error(self, mocker) -> None:
        # arrange
        system_id = 1234

        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            GetSystemService,
            'execute',
            side_effect=ServiceLayerNotFoundError('Exception mocked')
        )

        # act
        response = client.get(f'/{system_id}')

        # assert
        assert response.status_code == 404

    def test_get_exception_error(self, mocker) -> None:
        # arrange
        system_id = 1234

        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            GetSystemService,
            'execute',
            side_effect=Exception('Exception mocked')
        )
        # act

        response = client.get(f'/{system_id}')

        # assert
        assert response.status_code == 400

    def test_get_ok(self, mocker) -> None:
        # arrange
        system_id = 112314
        token_id = uuid4()
        name = "Sistema do Juvenal"

        system_return = SystemResponseServiceDto(system_id=system_id, token_id=token_id, system_name=name, status=StatusEnum.ACTIVE)

        mocker.patch.object(
            SystemRoute, 'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            GetSystemService,
            'execute',
            return_value=system_return
        )
        # act
        response = client.get(f'/{system_id}')

        # assert
        GetSystemService.execute.assert_called_once_with(
            repo=self.repo,
            system_id=system_id
        )
        assert response.status_code == 200

    def test_insert_exception_error(self, mocker) -> None:
        # arrange
        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            InsertSystemService,
            'execute',
            side_effect=Exception('Exception mocked')
        )
        # act
        response = client.post(
            '/',
            json={'system_name': 'Sistema Teste', 'token_id': '8c312158-2fa3-41c4-8b27-2204447ae3e0'}
        )

        # assert
        assert response.status_code == 400

    def test_insert_duplicated_name_error(self, mocker) -> None:
        # arrange
        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            InsertSystemService,
            'execute',
            side_effect=ServiceLayerDuplicatedNameError('Exception mocked')
        )
        # act
        response = client.post(
            '/',
            json={'system_name': 'Sistema Teste', 'token_id': '8c312158-2fa3-41c4-8b27-2204447ae3e0'}
        )

        # assert
        assert response.status_code == 400

    def test_insert_ok(self, mocker) -> None:
        # arrange
        token_id = UUID('8c312158-2fa3-41c4-8b27-2204447ae3e0')
        name = "Sistema Teste"
        system_id = 1234
        data = CreateSystemRequestServiceDto(
            token_id=token_id,
            system_name="Sistema Teste"
        )

        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            InsertSystemService,
            'execute',
            return_value=System(
                system_id=system_id,
                token_id=token_id,
                system_name=name
            )
        )

        # act
        response = client.post(
            '/',
            json={'system_name': 'Sistema Teste', 'token_id': '8c312158-2fa3-41c4-8b27-2204447ae3e0'}
        )

        # assert
        InsertSystemService.execute.assert_called_once_with(
            db=self.db,
            repo=self.repo,
            data=data
        )
        assert response.status_code == 201

    def test_list_exception_error(self, mocker) -> None:
        # arrange
        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            self_value=self.repo
        )

        mocker.patch.object(
            ListSystemService,
            'execute',
            side_effect=Exception('Exception mocked')
        )
        # act
        response = client.get('/')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_list_secondary_parameters_ok(self, mocker) -> None:
        # arrange
        max_records = 2
        system_status = StatusEnum.ACTIVE
        name = "Um nome Válido"
        data = ListSystemServiceRequestDTO(
            max_records=max_records,
            system_name=name,
            system_status=system_status
        )

        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            ListSystemService,
            'execute',
            return_value=[]
        )
        # act
        response = client.get(f'/?max_records={max_records}&system_status={system_status}&system_name={name}')

        # assert
        ListSystemService.execute.assert_called_once_with(
            repo=self.repo,
            data=data
        )
        assert response.status_code == 200


    def test_list_ok(self, mocker) -> None:
        # arrange
        data = ListSystemServiceRequestDTO()

        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            ListSystemService,
            'execute',
            return_value=[]
        )
        # act
        response = client.get('/')

        # assert
        ListSystemService.execute.assert_called_once_with(
            repo=self.repo,
            data=data
        )
        assert response.status_code == 200

    def test_delete_generic_error(self, mocker) -> None:
        # arrange
        system_id = 1234
        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            DeleteSystemService,
            'execute',
            side_effect=Exception('Mocked error')
        )
        # act
        response = client.delete(f'/{system_id}')

        # assert
        assert response.status_code == 400

    def test_delete_not_found_error(self, mocker) -> None:
        # arrange
        system_id = 1234
        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            DeleteSystemService,
            'execute',
            side_effect=ServiceLayerNotFoundError('Exception mocked')
        )

        # act
        response = client.delete(f'/{system_id}')

        # assert
        assert response.status_code == 404

    def test_delete_foreign_key_error(self, mocker) -> None:
        # arrange
        system_id = 1234
        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            DeleteSystemService,
            'execute',
            side_effect=ServiceLayerForeignKeyError('Exception mocked')
        )

        # act
        response = client.delete(f'/{system_id}')

        # assert
        assert response.status_code == 400

    def test_delete_ok(self, mocker) -> None:
        # arrange
        system_id = 1234

        mocker.patch.object(SystemRoute, 'create_function_repository', return_value=self.repo_function)
        mocker.patch.object(SystemRoute, 'create_paper_repository', return_value=self.repo_paper)
        mocker.patch.object(SystemRoute, 'create_owner_repository', return_value=self.repo_owner)
        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            DeleteSystemService,
            'execute'
        )
        # act
        response = client.delete(f'/{system_id}')

        # assert
        DeleteSystemService.execute.assert_called_once_with(
            db=self.db,
            repo=self.repo,
            paper_repo=self.repo_paper,
            owner_repo=self.repo_owner,
            function_repo=self.repo_function,
            system_id=system_id
        )
        assert response.status_code == 204

    def test_update_ok(self, mocker) -> None:
        # arrange
        system_id = 134
        name = 'Novo Nome'
        token_id = UUID('8c312158-2fa3-41c4-8b27-2204447ae3e0')

        data = UpdateSystemRequestServiceDto(system_name=name, token_id=token_id)

        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            UpdateSystemService,
            'execute'
        )
        # act
        response = client.put(
            f'/{system_id}',
            json={'system_name': 'Novo Nome', "token_id": "8c312158-2fa3-41c4-8b27-2204447ae3e0"}
        )

        # assert
        UpdateSystemService.execute.assert_called_once_with(
            data=data,
            repo=self.repo,
            system_id=system_id,
            db=self.db
        )
        assert response.status_code == 204

    def test_update_not_found_error(self, mocker) -> None:
        # arrange
        system_id = 134

        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            UpdateSystemService,
            'execute',
            side_effect=ServiceLayerNotFoundError('Exception mocked')
        )
        # act
        response = client.put(
            f'/{system_id}',
            json={'system_name': 'Novo Nome', "token_id": "8c312158-2fa3-41c4-8b27-2204447ae3e0"}
        )

        # assert
        assert response.status_code == 404

    def test_update_duplicated_name_error(self, mocker) -> None:
        # arrange
        system_id = 1234

        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            UpdateSystemService,
            'execute',
            side_effect=ServiceLayerDuplicatedNameError('Exception mocked')
        )
        # act
        response = client.put(
            f'/{system_id}',
            json={'system_name': 'Novo Nome', "token_id": "8c312158-2fa3-41c4-8b27-2204447ae3e0"}
        )

        # assert
        assert response.status_code == 400
    
    def test_update_generic_error(self, mocker) -> None:
        # arrange
        system_id = 1234

        mocker.patch.object(
            SystemRoute,
            'create_system_repository',
            return_value=self.repo
        )

        mocker.patch.object(
            UpdateSystemService,
            'execute',
            side_effect=Exception('Exception mocked')
        )
        # act
        response = client.put(
            f'/{system_id}',
            json={'system_name': 'Novo Nome', "token_id": "8c312158-2fa3-41c4-8b27-2204447ae3e0"}
        )

        # assert
        assert response.status_code == 400
