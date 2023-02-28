from dotenv import load_dotenv
from fastapi.testclient import TestClient
from src.domain.enums.function_type_enum import FunctionTypeEnum
from src.domain.enums.status_enum import StatusEnum

from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.repositories.implementations import (FunctionRepository,
                                                    SystemRepository,
                                                    FeatureRepository)
from src.services.DTOs.function.create_function_request_service_dto import CreateFunctionRequestServiceDto
from src.services.DTOs.function.update_function_request_service_dto import UpdateFunctionRequestServiceDto
from src.services.DTOs.function.function_response_service_dto import FunctionResponseServiceDto
from src.services.exceptions import (ServiceLayerDuplicatedNameError,
                                     ServiceLayerNotFoundError,
                                     ServiceLayerForeignKeyError)
from src.services.implementations.function import (DeleteFunctionService,
                                                   GetFunctionService,
                                                   InsertFunctionService,
                                                   ListFunctionService,
                                                   UpdateFunctionService)
from src.web_app.controllers.function_controller import (FunctionRoute,
                                                         function_route)
from src.services.DTOs.function.list_function_service_request_dto import ListFunctionServiceRequestDTO


client = TestClient(function_route)


class TesteFunctionController:

    def setup_class(self) -> None:
        load_dotenv()
        self.db = DbHandler(DbConfig())
        self.repo = FunctionRepository(self.db)
        self.system_repo = SystemRepository(self.db)
        self.feature_repo = FeatureRepository(self.db)

    def test_get_ok(self, mocker):
        # arrange
        function_id = 10

        function_return = FunctionResponseServiceDto(function_id=function_id, name="", function_type=FunctionTypeEnum.EXECUTION, system_id=1234, name_system="", status=StatusEnum.ACTIVE)

        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(GetFunctionService, "execute", return_value=function_return)

        # act
        response = client.get(f'/{function_id}')

        # assert
        GetFunctionService.execute.assert_called_once_with(repo=self.repo, id=function_id)
        assert response.status_code == 200

    # Tem que fazer o assert de se o get está fazendo o return da function? Como?

    def test_get_not_found_error(self, mocker):
        # arrange
        function_id = 10

        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(GetFunctionService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # act
        response = client.get(f'/{function_id}')

        # assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_generic_exception_error(self, mocker):
        # arrange
        function_id = 10
        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(GetFunctionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.get(f'/{function_id}')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_delete_ok(self, mocker):
        # arrange
        function_id = 10

        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(FunctionRoute, 'create_feature_repository', return_value=self.feature_repo)
        mocker.patch.object(DeleteFunctionService, "execute")

        # act
        response = client.delete(f'/{function_id}')

        # assert
        DeleteFunctionService.execute.assert_called_once_with(db=self.db, repo=self.repo, feature_repo=self.feature_repo, id=function_id)
        assert response.status_code == 204

    def test_delete_foreign_key_error(self, mocker):
        # arrange
        function_id = 10

        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(FunctionRoute, 'create_feature_repository', return_value=self.feature_repo)
        mocker.patch.object(DeleteFunctionService, "execute", side_effect=ServiceLayerForeignKeyError('Exception mocked'))

        # act
        response = client.delete(f'/{function_id}')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_delete_not_found_error(self, mocker):
        # arrange
        function_id = 10

        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(FunctionRoute, 'create_feature_repository', return_value=self.feature_repo)
        mocker.patch.object(DeleteFunctionService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # act
        response = client.delete(f'/{function_id}')

        # assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_delete_generic_exception_error(self, mocker):
        # arrange
        function_id = 10

        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(FunctionRoute, 'create_feature_repository', return_value=self.feature_repo)
        mocker.patch.object(DeleteFunctionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.delete(f'/{function_id}')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    # ver se valores dados dos parâmetros estão sendo chamados ok
    def test_get_all_parameters_ok(self, mocker):
        # arrange
        max_records = 3
        system_id = 1234
        function_name = "name123456"
        function_type = FunctionTypeEnum.EXECUTION
        data = ListFunctionServiceRequestDTO(max_records=max_records, system_id=system_id, function_name=function_name, function_type=function_type)

        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(ListFunctionService, "execute", return_value=[])

        # act
        response = client.get(f'/?max_records={max_records}&system_id={system_id}&function_name={function_name}&function_type={function_type}')

        # assert
        ListFunctionService.execute.assert_called_once_with(repo=self.repo, data=data)
        assert response.status_code == 200

    # ver se os valores padrões dos parâmetros estão sendo respeitados ok
    def test_get_all_default_values_ok(self, mocker):
        # arrange
        data = ListFunctionServiceRequestDTO(max_records=0, system_id=None, function_name=None, function_type=None)

        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(ListFunctionService, "execute", return_value=[])

        # act
        response = client.get('/')

        # assert
        ListFunctionService.execute.assert_called_once_with(repo=self.repo, data=data)
        assert response.status_code == 200

    # test str para max_records, function_type e function_status error?

    # generic exception error
    def test_get_all_generic_exception_error(self, mocker):
        # arrange
        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(ListFunctionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.get('/')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    # assert se o get_all tá fazendo retorno da lista? Como??

    # assert called once InsertFunctionService.execute(db=db_, repo=FunctionRoute.create_function_repository(db_), system_id=system_id , function_name=function_name , function_type=function_type) ok
    def test_insert_ok(self, mocker):
        # arrange
        system_id = 1234
        name = "nomenovonomenovo"
        create_function = CreateFunctionRequestServiceDto(system_id=system_id, name=name, function_type=FunctionTypeEnum.REGISTRATION)
        created_function = FunctionResponseServiceDto(name=name, function_type=FunctionTypeEnum.EXECUTION, system_id=system_id, function_id=1, name_system="name_system", status=StatusEnum.ACTIVE)

        mocker.patch.object(FunctionRoute, 'create_system_repository', return_value=self.system_repo)
        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(InsertFunctionService, "execute", return_value=created_function)

        # act
        response = client.post('/', json={"system_id": str(system_id), "name": name, "function_type": "1"})

        # assert
        InsertFunctionService.execute.assert_called_once_with(db=self.db, repo=self.repo, system_repo=self.system_repo, data=create_function)
        assert response.status_code == 201

    def test_insert_system_not_found_error(self, mocker):
        # arrange
        mocker.patch.object(InsertFunctionService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # act
        response = client.post('/', json={"system_id": "1234", "name": "nomenovonomenovo", "function_type": "1"})

        # assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    # ServiceLayerDuplicatedNameError
    def test_insert_duplicated_name_error(self, mocker):
        # arrange
        mocker.patch.object(InsertFunctionService, "execute", side_effect=ServiceLayerDuplicatedNameError('Exception mocked'))

        # act
        response = client.post('/', json={"system_id": "1234", "name": "nomenovonomenovo", "function_type": "1"})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    # generic exception error
    def test_insert_generic_exception_error(self, mocker):
        # arrange
        mocker.patch.object(InsertFunctionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.post('/', json={"system_id": "1234", "name": "nomenovonomenovo", "function_type": "1"})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    # assert se tá retornando new_function?

    # assert called once UpdateFunctionService.execute(db=db_, repo=FunctionRoute.create_function_repository(db_), id=function_id, new_system_id=new_system_id , new_name=new_function_name , new_function_type=new_function_type)
    def test_update_ok(self, mocker):
        # arrange
        function_id = 10
        function_name = "nomenovonomenovo"
        function_type = FunctionTypeEnum.REGISTRATION
        update_function_dto = UpdateFunctionRequestServiceDto(name=function_name, function_type=function_type)

        mocker.patch.object(FunctionRoute, 'create_function_repository', return_value=self.repo)
        mocker.patch.object(UpdateFunctionService, "execute")

        # act
        response = client.put(f'/{function_id}', json={"function_name": "nomenovonomenovo", "function_type": "1"})

        # assert
        UpdateFunctionService.execute.assert_called_once_with(db=self.db, repo=self.repo, id=function_id, data=update_function_dto)
        assert response.status_code == 204

    # ServiceLayerDuplicatedNameError
    def test_update_duplicated_name_error(self, mocker):
        # arrange
        function_id = 10

        mocker.patch.object(UpdateFunctionService, "execute", side_effect=ServiceLayerDuplicatedNameError('Exception mocked'))

        # act
        response = client.put(f'/{function_id}', json={"function_name": "nomenovonomenovo", "function_type": "1"})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    # ServiceLayerNotFoundError
    def test_update_not_found_error(self, mocker):
        # arrange
        function_id = 10

        mocker.patch.object(UpdateFunctionService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # act
        response = client.put(f'/{function_id}', json={"function_name": "nomenovonomenovo", "function_type": "1"})

        # assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    # generic exception error
    def test_update_generic_exception_error(self, mocker):
        # arrange
        function_id = 10

        mocker.patch.object(UpdateFunctionService, "execute", side_effect=Exception('Exception mocked'))

        # act
        response = client.put(f'/{function_id}', json={"function_name": "nomenovonomenovo", "function_type": "1"})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'
