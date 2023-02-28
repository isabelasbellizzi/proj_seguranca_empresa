from dotenv import load_dotenv
from fastapi.testclient import TestClient
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.repositories.implementations import \
    OwnerRepository, SystemRepository, UserRepository
from src.services.exceptions import ServiceLayerNotFoundError, ServiceLayerDuplicatedObjectError
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError
from src.services.implementations.owner import (DeleteOwnerService,
                                                GetOwnerService,
                                                GetSystemsOwnedService,
                                                ListOwnerService,
                                                InsertOwnerService)

from src.web_app.controllers import OwnerRoute, owner_route
from src.services.DTOs.owner import (
    CreateOwnerRequestServiceDto, OwnerResponseServiceDto, ListOwnerServiceRequestDTO)
from src.web_app.DTOs import MessageResponseDTO
from src.services.DTOs.system import SystemResponseServiceDto
from uuid import uuid4


client = TestClient(owner_route)


class TesteOwnerController:

    def setup_class(self) -> None:
        load_dotenv()
        self.db = DbHandler(DbConfig())
        self.repo = OwnerRepository(self.db)
        self.system_repo = SystemRepository(self.db)
        self.user_repo = UserRepository(self.db)
        
        
    ###CREATE###
    
    def test_insert_owner_404_not_found_error(self, mocker):
        # Arrange
        user_id = 1234
        system_id = 1234
        data = CreateOwnerRequestServiceDto(system_id=system_id, user_id=user_id)

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(OwnerRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(OwnerRoute, 'create_user_repository', return_value=self.user_repo)
        mocker.patch.object(InsertOwnerService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.post('/', json={"user_id": str(user_id), "system_id": system_id})

        # Assert
        InsertOwnerService.execute.assert_called_once_with(db=self.db, repo=self.repo, user_repo=self.user_repo, system_repo=self.system_repo, data=data)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'
        

    def test_insert_owner_400_duplicated_error(self, mocker):
        # Arrange
        user_id = 1234
        system_id = 1234
        data = CreateOwnerRequestServiceDto(system_id=system_id, user_id=user_id)

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(OwnerRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(OwnerRoute, 'create_user_repository', return_value=self.user_repo)
        mocker.patch.object(InsertOwnerService, "execute", side_effect=ServiceLayerDuplicatedObjectError('Exception mocked'))

        # Act
        response = client.post('/', json={"user_id": str(user_id), "system_id": system_id})

        # Assert
        InsertOwnerService.execute.assert_called_once_with(db=self.db, repo=self.repo, user_repo=self.user_repo, system_repo=self.system_repo, data=data)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'
   
    def test_insert_owner_400_bad_request_error(self, mocker):
        # Arrange
        user_id = 1234
        system_id = 1234
        data = CreateOwnerRequestServiceDto(system_id=system_id, user_id=user_id)

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(OwnerRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(OwnerRoute, 'create_user_repository', return_value=self.user_repo)
        mocker.patch.object(InsertOwnerService, "execute", side_effect=Exception('Exception mocked'))

        # Act
        response = client.post('/', json={"user_id": str(user_id), "system_id": system_id})

        # Assert
        InsertOwnerService.execute.assert_called_once_with(db=self.db, repo=self.repo, user_repo=self.user_repo, system_repo=self.system_repo, data=data)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    ###READ###

    def test_get_owner_404_not_found_error(self, mocker):
        # Arrange
        owner_id = 1

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(GetOwnerService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.get(f'/{owner_id}')

        # Assert
        GetOwnerService.execute.assert_called_once_with(repo=self.repo, owner_id=owner_id)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'


    def test_get_owner_400_generic_exception_error(self, mocker):
        # Arrange
        owner_id = 1

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(GetOwnerService, "execute", side_effect=Exception('Exception mocked'))

        # Act
        response = client.get(f'/{owner_id}')

        # Assert
        GetOwnerService.execute.assert_called_once_with(repo=self.repo, owner_id=owner_id)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'


    def test_get_owner_200_ok(self, mocker):
        # Arrange
        owner_id = 1
        owner_return = OwnerResponseServiceDto(system_id=1, user_id=1, owner_id=owner_id, user_email="email@teste.com", system_name="System", status=StatusEnum.ACTIVE)

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(GetOwnerService, "execute", return_value=owner_return)

        # Act
        response = client.get(f'/{owner_id}')

        # Assert
        GetOwnerService.execute.assert_called_once_with(repo=self.repo, owner_id=owner_id)
        assert response.status_code == 200

    def test_get_all_owners_400_generic_exception_error(self, mocker):
        # Arrange
        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(ListOwnerService, "execute", side_effect=Exception('Exception mocked'))

        # Act
        response = client.get('/')

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_all_owners_200_default_parameters_ok(self, mocker):
        # Arrange
        owner_return = OwnerResponseServiceDto(system_id=1, user_id=1, owner_id=1, user_email="email@teste.com", system_name="System", status=StatusEnum.ACTIVE)
        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(ListOwnerService, "execute", return_value=[owner_return])
        list_owner_dto = ListOwnerServiceRequestDTO(max_records=0, user_id= None, system_id= None)

        # Act
        response = client.get('/')

        # Assert
        ListOwnerService.execute.assert_called_once_with(repo=self.repo, data=list_owner_dto)
        assert response.status_code == 200

    def test_get_all_owners_200_parameters_ok(self, mocker):
        # Arrange
        max_records = 1
        user_id = 1
        system_id = 1
        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(ListOwnerService, "execute", return_value=[])
        list_owner_dto = ListOwnerServiceRequestDTO(max_records=max_records, user_id=user_id, system_id=system_id)

        # Act
        response = client.get(f'/?max_records={max_records}&user_id={user_id}&system_id={system_id}')

        # Assert
        ListOwnerService.execute.assert_called_once_with(repo=self.repo, data=list_owner_dto)
        assert response.status_code == 200

    def test_get_systems_owned_404_not_found(self, mocker):
        # Arrange
        user_email = "email@teste.com"

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(OwnerRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(OwnerRoute, 'create_user_repository', return_value=self.user_repo)
        mocker.patch.object(GetSystemsOwnedService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.get(f'/systems/{user_email}')

        # Assert
        GetSystemsOwnedService.execute.assert_called_once_with(repo=self.repo, system_repo=self.system_repo, user_repo=self.user_repo, user_email=user_email)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_systems_owned_400_generic_exception_error(self, mocker):
        # Arrange
        user_email = "email@teste.com"

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(OwnerRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(OwnerRoute, 'create_user_repository', return_value=self.user_repo)
        mocker.patch.object(GetSystemsOwnedService, "execute", side_effect=Exception('Exception mocked'))

        # Act
        response = client.get(f'/systems/{user_email}')

        # Assert
        GetSystemsOwnedService.execute.assert_called_once_with(repo=self.repo, system_repo=self.system_repo, user_repo=self.user_repo, user_email=user_email)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_systems_owned_200_ok(self, mocker):
        # Arrange
        user_email = "email@teste.com"
        token_id = uuid4()
        system_name = "name"
        system_id = 1
        return_system = SystemResponseServiceDto(token_id=token_id, system_name=system_name, system_id=system_id, status=StatusEnum.ACTIVE)

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(OwnerRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(OwnerRoute, 'create_user_repository', return_value=self.user_repo)
        mocker.patch.object(GetSystemsOwnedService, "execute", return_value=[return_system])

        # Act
        response = client.get(f'/systems/{user_email}')

        # Assert
        GetSystemsOwnedService.execute.assert_called_once_with(repo=self.repo, system_repo=self.system_repo,user_repo=self.user_repo, user_email=user_email)
        assert response.status_code == 200
        

    ###DELETE###
    
    def test_delete_systems_owned_404_not_found_error(self, mocker):
        # Arrange
        owner_id = 1234

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(DeleteOwnerService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.delete(f'/{owner_id}')

        # Assert
        DeleteOwnerService.execute.assert_called_once_with(db=self.db, repo=self.repo, owner_id=owner_id)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'


    def test_delete_systems_owned_200_generic_error(self, mocker):
        # Arrange
        owner_id = 1234

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(DeleteOwnerService, "execute", side_effect=Exception('Exception mocked'))

        # Act
        response = client.delete(f'/{owner_id}')

        # Assert
        DeleteOwnerService.execute.assert_called_once_with(db=self.db, repo=self.repo, owner_id=owner_id)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'


    def test_delete_systems_owned_204_ok(self, mocker):
        # Arrange
        owner_id = 1234

        mocker.patch.object(OwnerRoute, 'create_owner_repository', return_value=self.repo)
        mocker.patch.object(DeleteOwnerService, "execute")

        # Act
        response = client.delete(f'/{owner_id}')

        # Assert
        DeleteOwnerService.execute.assert_called_once_with(db=self.db, repo=self.repo, owner_id=owner_id)
        assert response.status_code == 204