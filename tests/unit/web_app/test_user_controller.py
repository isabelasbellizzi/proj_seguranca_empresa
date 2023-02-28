from uuid import uuid4

from dotenv import load_dotenv
from fastapi.testclient import TestClient

from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.repositories.implementations.user_repository import \
    UserRepository
from src.services.DTOs.user import (CreateUserRequestServiceDto,
                                    UpdateUserRequestServiceDto,
                                    UserResponseServiceDto)
from src.services.exceptions.service_layer_duplicated_name_error import \
    ServiceLayerDuplicatedNameError
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError
from src.services.implementations.user import (DeleteUserService,
                                               GetUserByIdService,
                                               GetUserByEmailService,
                                               InsertUserService,
                                               ListUserService,
                                               UpdateUserService)
from src.web_app.controllers.user_controller import UserRoute, user_route
from src.infra.repositories.implementations.user_permission_repository import UserPermissionRepository
from src.infra.repositories.implementations.owner_repository import OwnerRepository


client = TestClient(user_route)


class TesteUserController:

    def setup_class(self) -> None:
        load_dotenv()
        self.db = DbHandler(DbConfig())  # pylint: disable=attribute-defined-outside-init
        self.repo = UserRepository(self.db)  # pylint: disable=attribute-defined-outside-init
        self.up_repo = UserPermissionRepository(self.db)  # pylint: disable=attribute-defined-outside-init
        self.owner_repo = OwnerRepository(self.db)  # pylint: disable=attribute-defined-outside-init


    ###CREATE###


    def test_insert_generic_exception_error(self, mocker):
        # Arrange
        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(InsertUserService, "execute", side_effect=Exception('Exception mocked'))

        # Act
        response = client.post('/', json={"azure_id": "8c312158-2fa3-41c4-8b27-2204447ae3e0", "user_email": "teste@teste.com"})

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'


    def test_insert_duplicated_name_error(self, mocker):
        # Arrange
        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(InsertUserService, "execute", side_effect=ServiceLayerDuplicatedNameError('Exception mocked'))

        # Act
        response = client.post('/', json={"azure_id": "8c312158-2fa3-41c4-8b27-2204447ae3e0", "user_email": "teste@teste.com"})

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_insert_ok(self, mocker):
        # Arrange
        test_azure = uuid4()
        test_email = "teste@unitario.com"

        create_user = CreateUserRequestServiceDto(azure_id=test_azure, user_email=test_email)
        new_user = UserResponseServiceDto(user_id=1234, azure_id=test_azure, user_email=test_email, status=StatusEnum.ACTIVE)

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(UserRoute, 'create_user_dto', return_value=create_user)
        mocker.patch.object(InsertUserService, "execute", return_value=new_user)

        # Act
        response = client.post('/', json={"azure_id": str(test_azure), "user_email": test_email})

        # Assert
        InsertUserService.execute.assert_called_once_with(db=self.db, repo=self.repo, data=create_user)
        assert response.status_code == 201


    ###READ###


    def test_get_generic_exception_error(self, mocker):
        # Arrange
        test_id = 1234

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(GetUserByIdService, 'execute', side_effect=Exception('Exception mocked'))

        # Act
        response = client.get(f'/{test_id}')

        # Assert
        GetUserByIdService.execute.assert_called_once_with(repo=self.repo, user_id=test_id)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_not_found_error(self, mocker):
        # Arrange
        test_id = 1234

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(GetUserByIdService, 'execute', side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.get(f'/{test_id}')

        # Assert
        GetUserByIdService.execute.assert_called_once_with(repo=self.repo, user_id=test_id)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_ok(self, mocker):
        # Arrange
        test_id = 1234
        test_user_return = UserResponseServiceDto(user_id=test_id, azure_id=uuid4(), user_email="", status=StatusEnum.ACTIVE)  # type: ignore

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(GetUserByIdService, 'execute', return_value=test_user_return)

        #act
        response = client.get(f'/{test_id}')

        # assert
        GetUserByIdService.execute.assert_called_once_with(repo=self.repo, user_id=test_id)
        assert response.status_code == 200

    def test_get_by_email_generic_exception_error(self, mocker):
        # Arrange
        test_email = "email@email.com"

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(GetUserByEmailService, 'execute', side_effect=Exception('Exception mocked'))

        # Act
        response = client.get(f'/email/{test_email}')

        # Assert
        GetUserByEmailService.execute.assert_called_once_with(repo=self.repo, user_email=test_email)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_by_email_found_error(self, mocker):
        # Arrange
        test_email = "email@email.com"

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(GetUserByEmailService, 'execute', side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.get(f'/email/{test_email}')

        # Assert
        GetUserByEmailService.execute.assert_called_once_with(repo=self.repo, user_email=test_email)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_by_email_ok(self, mocker):
        # Arrange
        test_email = "email@email.com"
        test_user_return = UserResponseServiceDto(user_id=1234, azure_id=uuid4(), user_email=test_email, status=StatusEnum.ACTIVE)  # type: ignore

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(GetUserByEmailService, 'execute', return_value=test_user_return)

        #act
        response = client.get(f'/email/{test_email}')

        # assert
        GetUserByEmailService.execute.assert_called_once_with(repo=self.repo, user_email=test_email)
        assert response.status_code == 200

    def test_get_all_generic_exception_error(self, mocker):
        # Arrange
        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(ListUserService, 'execute', side_effect=Exception('Exception mocked'))

        # Act
        response = client.get('/')

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'


    def test_get_all_ok(self, mocker):
        # Arrange
        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(ListUserService, 'execute', return_value=[])

        # Act
        response = client.get('/')

        # Assert
        ListUserService.execute.assert_called_once_with(repo=self.repo, max_records=0)
        assert response.status_code == 200


    ###UPDATE###


    def test_update_generic_exception_error(self, mocker):
        # Arrange
        test_id = 1234

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(UpdateUserService, 'execute', side_effect=Exception('Exception mocked'))

        # Act
        response = client.put(f'/{test_id}', json={"azure_id": "8c312158-2fa3-41c4-8b27-2204447ae3e0", "user_email": "teste@teste.com"})

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_update_not_found_error(self, mocker):
        # Arrange
        test_id = 1234

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(UpdateUserService, 'execute', side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.put(f'/{test_id}', json={"azure_id": "8c312158-2fa3-41c4-8b27-2204447ae3e0", "user_email": "teste@teste.com"})

        # Assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_update_duplicated_name_error(self, mocker):
        # Arrange
        test_id = 1234

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(UpdateUserService, 'execute', side_effect=ServiceLayerDuplicatedNameError('Exception mocked'))

        # Act
        response = client.put(f'/{test_id}', json={"azure_id": "8c312158-2fa3-41c4-8b27-2204447ae3e0", "user_email": "teste@teste.com"})

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_update_ok(self, mocker):
        # Arrange
        test_id = 1234
        test_azure = uuid4()
        test_email = "teste@unitario.com"
        update_user_dto = UpdateUserRequestServiceDto(azure_id=test_azure, user_email=test_email)  # type: ignore

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(UpdateUserService, 'execute')

        # Act
        response = client.put(f'/{test_id}', json={"azure_id": str(test_azure), "user_email": test_email})

        # Assert
        UpdateUserService.execute.assert_called_once_with(db=self.db, repo=self.repo, user_id=test_id, data=update_user_dto)
        assert response.status_code == 204


    ###DELETE###

    def test_delete_generic_exception_error(self, mocker):
        # Arrange
        test_id = 1234

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(UserRoute, 'create_user_permission_repository', return_value=self.up_repo)
        mocker.patch.object(UserRoute, 'create_owner_repository', return_value=self.owner_repo)
        mocker.patch.object(DeleteUserService, 'execute', side_effect=Exception('Exception mocked'))

        # Act
        response = client.delete(f'/{test_id}')

        # Assert
        DeleteUserService.execute.assert_called_once_with(db=self.db, repo=self.repo, up_repo=self.up_repo, owner_repo=self.owner_repo, user_id=test_id)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'


    def test_delete_not_found_error(self, mocker):
        # Arrange
        test_id = 1234

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(UserRoute, 'create_user_permission_repository', return_value=self.up_repo)
        mocker.patch.object(UserRoute, 'create_owner_repository', return_value=self.owner_repo)
        mocker.patch.object(DeleteUserService, 'execute', side_effect=ServiceLayerNotFoundError('Exception mocked'))


        # Act
        response = client.delete(f'/{test_id}')

        # Assert
        DeleteUserService.execute.assert_called_once_with(db=self.db, repo=self.repo, up_repo=self.up_repo, owner_repo=self.owner_repo, user_id=test_id)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'


    def test_delete_ok(self, mocker):
        # Arrange
        test_id = 1234

        mocker.patch.object(UserRoute, 'create_user_repository', return_value=self.repo)
        mocker.patch.object(UserRoute, 'create_user_permission_repository', return_value=self.up_repo)
        mocker.patch.object(UserRoute, 'create_owner_repository', return_value=self.owner_repo)
        mocker.patch.object(DeleteUserService, 'execute')

        # Act
        response = client.delete(f'/{test_id}')

        # Assert
        DeleteUserService.execute.assert_called_once_with(db=self.db, repo=self.repo, up_repo=self.up_repo, owner_repo=self.owner_repo, user_id=test_id)
        assert response.status_code == 204
