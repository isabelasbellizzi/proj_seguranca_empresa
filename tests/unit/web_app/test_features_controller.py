from dotenv import load_dotenv
from fastapi.testclient import TestClient

from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.repositories.implementations.features_repository import \
    FeatureRepository
from src.infra.repositories.implementations.function_repository import FunctionRepository
from src.infra.repositories.implementations.paper_repository import PaperRepository
from src.services.DTOs.feature import CreateFeatureRequestServiceDto, FeatureResponseServiceDto, UpdateFeatureRequestServiceDto, ListFeatureServiceRequestDTO

from src.services.exceptions.service_layer_duplicated_name_error import \
    ServiceLayerDuplicatedNameError
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError
from src.services.implementations.feature import (DeleteFeatureService,
                                                  GetFeatureService,
                                                  InsertFeatureService,
                                                  ListFeatureService,
                                                  UpdateFeatureService)

from src.web_app.controllers.features_controller import FeatureRoute, feature_route

client = TestClient(feature_route)


class TestFeatureController:

    def setup_class(self) -> None:
        load_dotenv()
        self.db = DbHandler(DbConfig())  # pylint: disable=attribute-defined-outside-init
        self.repo = FeatureRepository(self.db)  # pylint: disable=attribute-defined-outside-init
        self.function_repo = FunctionRepository(self.db)  # pylint: disable=attribute-defined-outside-init
        self.paper_repo = PaperRepository(self.db)  # pylint: disable=attribute-defined-outside-init


    def test_insert_generic_exception_error(self, mocker):
        # Arrange
        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(InsertFeatureService, "execute", side_effect=Exception('Exception mocked'))

        # Act
        response = client.post('/', json={"paper_id": "100",
                                          "function_id": "300",
                                          "create": "true",
                                          "read": "true",
                                          "update": "true",
                                          "delete": "true"})

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'


    def test_insert_duplicated_name_error(self, mocker):
        # Arrange
        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(InsertFeatureService, "execute", side_effect=ServiceLayerDuplicatedNameError('Exception mocked'))

        # Act
        response = client.post('/', json={"paper_id": "100",
                                          "function_id": "300",
                                          "create": "true",
                                          "read": "true",
                                          "update": "true",
                                          "delete": "true"})

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_function_not_found_error(self, mocker):
        # Arrange
        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(InsertFeatureService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.post('/', json={"paper_id": "100",
                                          "function_id": "300",
                                          "create": "true",
                                          "read": "true",
                                          "update": "true",
                                          "delete": "true"})

        # Assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_insert_ok(self, mocker):
        # Arrange
        paper_id = 100
        feature_id = 200
        function_id = 300
        paper_name = "Paper teste"
        function_name = "Function teste"
        system_name = "System teste"
        create = True
        read = True
        update = True
        delete = True

        create_feature = CreateFeatureRequestServiceDto(paper_id=paper_id, function_id=function_id, create=create, read=read, update=update, delete=delete)
        new_feature = FeatureResponseServiceDto(paper_id=paper_id, function_id=function_id, create=create, read=read, update=update, delete=delete, status=StatusEnum.ACTIVE, feature_id=feature_id, paper_name=paper_name, system_name=system_name, function_name=function_name)

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(FeatureRoute, 'create_paper_repository', return_value=self.paper_repo)
        mocker.patch.object(FeatureRoute, 'create_function_repository', return_value=self.function_repo)
        mocker.patch.object(FeatureRoute, 'create_feature_dto', return_value=create_feature)
        mocker.patch.object(InsertFeatureService, "execute", return_value=new_feature)

        # Act
        response = client.post('/', json={"paper_id": "100",
                                          "function_id": "300",
                                          "create": "true",
                                          "read": "true",
                                          "update": "true",
                                          "delete": "true"})


        # Assert
        InsertFeatureService.execute.assert_called_once_with(db=self.db, repo=self.repo, function_repo=self.function_repo, paper_repo=self.paper_repo, data=create_feature)
        assert response.status_code == 201


    ###READ###


    def test_get_generic_exception_error(self, mocker):
        # Arrange
        test_feature_id = 900

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(GetFeatureService, 'execute', side_effect=Exception('Exception mocked'))

        # Act
        response = client.get(f'/{test_feature_id}')

        # Assert
        GetFeatureService.execute.assert_called_once_with(repo=self.repo, id=test_feature_id)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_not_found_error(self, mocker):
        # Arrange
        test_feature_id = 900

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(GetFeatureService, 'execute', side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.get(f'/{test_feature_id}')

        # Assert
        GetFeatureService.execute.assert_called_once_with(repo=self.repo, id=test_feature_id)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_ok(self, mocker):
        # Arrange
        paper_id = 100
        feature_id = 200
        function_id = 300
        test_feature_id = 900
        paper_name = "Paper teste"
        function_name = "Function teste"
        system_name = "System teste"
        create = True
        read = True
        update = True
        delete = True
        test_feature_return = FeatureResponseServiceDto(paper_id=paper_id, function_id=function_id, create=create, read=read, update=update, delete=delete, status=StatusEnum.ACTIVE, feature_id=feature_id, paper_name=paper_name, system_name=system_name, function_name=function_name)

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(GetFeatureService, 'execute', return_value=test_feature_return)

        #act
        response = client.get(f'/{test_feature_id}')

        # assert
        GetFeatureService.execute.assert_called_once_with(repo=self.repo, id=test_feature_id)
        assert response.status_code == 200

    def test_get_all_generic_exception_error(self, mocker):
        # Arrange
        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(ListFeatureService, 'execute', side_effect=Exception('Exception mocked'))

        # Act
        response = client.get('/')

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'


    def test_get_all_default_parameters_ok(self, mocker):
        # Arrange
        list_feature_request_dto = ListFeatureServiceRequestDTO(paper_id=None, function_id=None, max_records=0)

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(ListFeatureService, 'execute', return_value=[])

        # Act
        response = client.get('/')

        # Assert
        ListFeatureService.execute.assert_called_once_with(repo=self.repo, data=list_feature_request_dto)
        assert response.status_code == 200

    def test_get_all_parameters_ok(self, mocker):
        # arrange
        max_records = 1
        paper_id = 2
        function_id = 3

        list_feature_request_dto = ListFeatureServiceRequestDTO(paper_id=paper_id, function_id=function_id, max_records=max_records)

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(ListFeatureService, "execute", return_value=[])

        # act
        response = client.get(f'/?max_records={max_records}&paper_id={paper_id}&function_id={function_id}')

        # assert
        ListFeatureService.execute.assert_called_once_with(repo=self.repo, data=list_feature_request_dto)
        assert response.status_code == 200


    ###UPDATE###


    def test_update_generic_exception_error(self, mocker):
        # Arrange
        test_feature_id = 900

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(UpdateFeatureService, 'execute', side_effect=Exception('Exception mocked'))

        # Act
        response = client.put(f'/{test_feature_id}', json={"paper_id": "100",
                                                           "function_id": "300",
                                                           "create": "true",
                                                           "read": "true",
                                                           "update": "true",
                                                           "delete": "true"})

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_update_not_found_error(self, mocker):
        # Arrange
        test_feature_id = 900

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(UpdateFeatureService, 'execute', side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.put(f'/{test_feature_id}', json={"paper_id": "100",
                                                           "function_id": "300",
                                                           "create": "true",
                                                           "read": "true",
                                                           "update": "true",
                                                           "delete": "true"})

        # Assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_update_duplicated_name_error(self, mocker):
        # Arrange
        test_feature_id = 900

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(UpdateFeatureService, 'execute', side_effect=ServiceLayerDuplicatedNameError('Exception mocked'))

        # Act
        response = client.put(f'/{test_feature_id}', json={"paper_id": "100",
                                                           "function_id": "300",
                                                           "create": "true",
                                                           "read": "true",
                                                           "update": "true",
                                                           "delete": "true"})

        # Assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_update_ok(self, mocker):
        # Arrange
        test_feature_id = 900
        create = True
        read = True
        update = True
        delete = True
        update_test_dto = UpdateFeatureRequestServiceDto(create=create, read=read, update=update, delete=delete)

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(UpdateFeatureService, 'execute')

        # Act
        response = client.put(f'/{test_feature_id}', json={"create": "true",
                                                           "read": "true",
                                                           "update": "true",
                                                           "delete": "true"})

        # Assert
        UpdateFeatureService.execute.assert_called_once_with(db=self.db, repo=self.repo, feature_id=test_feature_id, data=update_test_dto)
        assert response.status_code == 204

    ###DELETE###


    def test_delete_generic_exception_error(self, mocker):
        # Arrange
        test_feature_id = 900

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(DeleteFeatureService, 'execute', side_effect=Exception('Exception mocked'))

        # Act
        response = client.delete(f'/{test_feature_id}')

        # Assert
        DeleteFeatureService.execute.assert_called_once_with(db=self.db, repo=self.repo, feature_id=test_feature_id)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'


    def test_delete_not_found_error(self, mocker):
        # Arrange
        test_feature_id = 900

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(DeleteFeatureService, 'execute', side_effect=ServiceLayerNotFoundError('Exception mocked'))

        # Act
        response = client.delete(f'/{test_feature_id}')

        # Assert
        DeleteFeatureService.execute.assert_called_once_with(db=self.db, repo=self.repo, feature_id=test_feature_id)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'


    def test_delete_ok(self, mocker):
        # Arrange
        test_feature_id = 900

        mocker.patch.object(FeatureRoute, 'create_feature_repository', return_value=self.repo)
        mocker.patch.object(DeleteFeatureService, 'execute')

        # Act
        response = client.delete(f'/{test_feature_id}')

        # Assert
        DeleteFeatureService.execute.assert_called_once_with(db=self.db, repo=self.repo, feature_id=test_feature_id)
        assert response.status_code == 204
