from dotenv import load_dotenv
from fastapi.testclient import TestClient
from src.domain.enums.status_enum import StatusEnum
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.repositories.implementations import \
    PaperRepository, UserPermissionRepository, FeatureRepository, SystemRepository
from src.services.exceptions.service_layer_duplicated_name_error import \
    ServiceLayerDuplicatedNameError
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError
from src.services.implementations.paper import (DeletePaperService,
                                                GetPaperService,
                                                InsertPaperService,
                                                ListPaperService,
                                                UpdatePaperService)
from src.web_app.controllers import PaperRoute, paper_route
from src.services.DTOs.paper import (PaperResponseServiceDto, CreatePaperRequestServiceDto,
                                     UpdatePaperRequestServiceDto, ListPaperServiceRequestDTO)


client = TestClient(paper_route)


class TesteFunctionController:

    def setup_class(self) -> None:
        load_dotenv()

    def test_get_ok(self, mocker):
        # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db)
        paper_id = 7
        paper_return = PaperResponseServiceDto(paper_id=paper_id, name="", system_id=1234, name_system="", status=StatusEnum.ACTIVE)


        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(GetPaperService, "execute", return_value=paper_return)

        #act
        response = client.get(f'/{paper_id}')

        # assert
        GetPaperService.execute.assert_called_once_with(repo=repo, paper_id=paper_id)
        assert response.status_code == 200

    def test_get_not_found_error(self, mocker):
        # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db)
        paper_id = 7

        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(GetPaperService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        #act
        response = client.get(f'/{paper_id}')

        # assert
        GetPaperService.execute.assert_called_once_with(repo=repo, paper_id=paper_id)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_generic_exception_error(self, mocker):
        # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db)
        paper_id = 7

        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(GetPaperService, "execute", side_effect=Exception('Exception mocked'))

        #act
        response = client.get(f'/{paper_id}')

        # assert
        GetPaperService.execute.assert_called_once_with(repo=repo, paper_id=paper_id)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_delete_ok(self, mocker):

        # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        user_per_repo = UserPermissionRepository(db=db)
        feature_repo = FeatureRepository(db=db)
        paper_id = 7

        mocker.patch.object(PaperRoute, 'create_user_permission_repository', return_value=user_per_repo)
        mocker.patch.object(PaperRoute, 'create_feature_repository', return_value=feature_repo)
        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(DeletePaperService, "execute")

        #act
        response = client.delete(f'/{paper_id}')

        # assert
        DeletePaperService.execute.assert_called_once_with(db=db, repo=repo, user_per_repo=user_per_repo, feature_repo=feature_repo, paper_id=paper_id)
        assert response.status_code == 204

    def test_delete_not_found_error(self, mocker):
        # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        user_per_repo = UserPermissionRepository(db=db)
        feature_repo = FeatureRepository(db=db)
        paper_id = 7

        mocker.patch.object(PaperRoute, 'create_user_permission_repository', return_value=user_per_repo)
        mocker.patch.object(PaperRoute, 'create_feature_repository', return_value=feature_repo)
        mocker.patch.object(PaperRoute, 'create_feature_repository', return_value=feature_repo)
        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(DeletePaperService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        #act
        response = client.delete(f'/{paper_id}')

        # assert
        DeletePaperService.execute.assert_called_once_with(db=db, repo=repo, user_per_repo=user_per_repo, feature_repo=feature_repo, paper_id=paper_id)
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_delete_generic_exception_error(self, mocker):
        # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        user_per_repo = UserPermissionRepository(db=db)
        feature_repo = FeatureRepository(db=db)
        paper_id = 7

        mocker.patch.object(PaperRoute, 'create_user_permission_repository', return_value=user_per_repo)
        mocker.patch.object(PaperRoute, 'create_feature_repository', return_value=feature_repo)
        mocker.patch.object(PaperRoute, 'create_feature_repository', return_value=feature_repo)
        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(DeletePaperService, "execute", side_effect=Exception('Exception mocked'))

        #act
        response = client.delete(f'/{paper_id}')

        # assert
        DeletePaperService.execute.assert_called_once_with(db=db, repo=repo, user_per_repo=user_per_repo, feature_repo=feature_repo, paper_id=paper_id)
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_get_all_parameters_ok(self, mocker):
    # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        data = ListPaperServiceRequestDTO(max_records=0, system_id=None, paper_name=None, paper_status=None)

        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(ListPaperService, "execute", return_value=[])

        #act
        response = client.get('/')

        # assert
        ListPaperService.execute.assert_called_once_with(repo=repo, data=data)
        assert response.status_code == 200

    def test_get_all_generic_exception_error(self, mocker):
    # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(ListPaperService, "execute", side_effect=Exception('Exception mocked'))

        #act
        response = client.get('/')

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_insert_ok(self, mocker):
    # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        system_repo = SystemRepository(db=db)
        system_id = 1234
        name = "nomenovonomenovo"
        paper_id = 10

        create_paper = CreatePaperRequestServiceDto(system_id=system_id, name=name)
        created_paper = PaperResponseServiceDto(name=name, system_id=system_id, paper_id=paper_id, name_system="name_system", status=StatusEnum.ACTIVE)

        mocker.patch.object(PaperRoute, 'create_system_repository', return_value=system_repo)
        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(PaperRoute, 'create_paper_dto', return_value=create_paper)
        mocker.patch.object(InsertPaperService, "execute", return_value=created_paper)

        #act
        response = client.post('/', json={"system_id": str(system_id), "paper_name": (name)})

        # assert
        InsertPaperService.execute.assert_called_once_with(db=db, repo=repo, system_repo=system_repo, data=create_paper)
        assert response.status_code == 201

    def test_insert_duplicated_name_error(self, mocker):
    # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)

        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(InsertPaperService, "execute", side_effect=ServiceLayerDuplicatedNameError('Exception mocked'))

        #act
        response = client.post('/', json={"system_id": "1234", "paper_name": "nomenovonomenovo"})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_insert_generic_exception_error(self, mocker):
    # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(InsertPaperService, "execute", side_effect=Exception('Exception mocked'))

        #act
        response = client.post('/', json={"system_id": "1234", "paper_name": "nomenovonomenovo"})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_update_ok(self, mocker):
        # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        paper_id = 10
        paper_name = "nomenovonomenovo"
        update_paper_dto = UpdatePaperRequestServiceDto(name=paper_name)

        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(UpdatePaperService, "execute")

        # act
        response = client.put(f'/{paper_id}', json={"paper_name": "nomenovonomenovo"})

        # assert
        UpdatePaperService.execute.assert_called_once_with(db=db, repo=repo, paper_id=paper_id, data=update_paper_dto)
        assert response.status_code == 204

    def test_update_duplicated_name_error(self, mocker):
    # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        paper_id = 10

        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(UpdatePaperService, "execute", side_effect=ServiceLayerDuplicatedNameError('Exception mocked'))

        #act
        response = client.put(f'/{paper_id}', json={"paper_name": "testeteste"})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'

    def test_update_not_found_error(self, mocker):
    # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        paper_id = 10

        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(UpdatePaperService, "execute", side_effect=ServiceLayerNotFoundError('Exception mocked'))

        #act
        response = client.put(f'/{paper_id}', json={"paper_name": "nomenovonomenovo"})

        # assert
        assert response.status_code == 404
        assert response.json()['msg'] == 'Exception mocked'

    def test_update_generic_exception_error(self, mocker):
    # arrange
        db = DbHandler(DbConfig())
        repo = PaperRepository(db=db)
        paper_id = 10

        mocker.patch.object(PaperRoute, 'create_paper_repository', return_value=repo)
        mocker.patch.object(UpdatePaperService, "execute", side_effect=Exception('Exception mocked'))

        #act
        response = client.put(f'/{paper_id}', json={"paper_name": "nomenovonomenovo"})

        # assert
        assert response.status_code == 400
        assert response.json()['msg'] == 'Exception mocked'
