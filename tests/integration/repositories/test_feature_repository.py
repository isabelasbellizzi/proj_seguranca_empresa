from dotenv import load_dotenv
import pytest
from src.domain.entities import Feature
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.orm.execute_mapping import execute_mapping
from src.infra.repositories.implementations import FeatureRepository
from src.services.DTOs.feature.list_feature_service_request_dto import ListFeatureServiceRequestDTO
from tests.integration.repositories import RepositoryBase, InsertManually

class TestFeatureRepository(RepositoryBase):
    def setup_class(self) -> None:
        load_dotenv()
        execute_mapping()
        self.db = DbHandler(DbConfig())
        self.db.open()
        self.session = self.db.get_session()
        self.repo = FeatureRepository(self.db)
        self.insert_manually = InsertManually()

    def test_get_not_found(self) -> None:
        feature_id = -1

        resp = self.repo.get(id=feature_id)

        assert resp == None

    def test_get_found(self) -> None:
        inserted_feature = self.insert_manually.feature(session=self.session)
        feature_id = inserted_feature.feature_id

        # act
        resp = self.repo.get(id=feature_id)

        # assert
        assert resp.feature_id == inserted_feature.feature_id
        assert resp.paper_id == inserted_feature.paper_id
        assert resp.function_id == inserted_feature.function_id
        assert resp.status == inserted_feature.status
        assert resp.create == inserted_feature.create
        assert resp.read == inserted_feature.read
        assert resp.update == inserted_feature.update
        assert resp.delete == inserted_feature.delete

    def test_add_ok(self) -> None:
        inserted_function = self.insert_manually.function(session=self.session)
        inserted_paper = self.insert_manually.paper(session=self.session)

        new_feature = Feature(paper_id=inserted_paper.paper_id, function_id=inserted_function.function_id)

        self.repo.add(new_feature=new_feature)

        resp = self.repo.get(id=new_feature.feature_id)

        assert resp.function_id != 0 or None
        assert resp.paper_id == inserted_paper.paper_id
        assert resp.function_id == inserted_function.function_id
        assert resp.status == 1
        assert resp.create == False
        assert resp.read == False
        assert resp.update == False
        assert resp.delete == False

    def test_delete_not_found(self) -> None:
        with pytest.raises(Exception) as error:
            self.repo.delete(id=1234)

        assert str(error.value) == "Feature not found. [feature_id=1234]"

    def test_delete_found(self) -> None:
        inserted_feature = self.insert_manually.feature(session=self.session)

        self.repo.delete(id=inserted_feature.feature_id)

        assert self.repo.get(id=inserted_feature.feature_id) is None

    def test_update(self) -> None:
        inserted_feature = self.insert_manually.feature(session=self.session)

        feature = self.repo.get(id=inserted_feature.feature_id)

        feature.create = True
        feature.read = True
        feature.update = True
        feature.delete = True

        self.repo.update(feature=feature)

        resp = self.repo.get(id=inserted_feature.feature_id)

        assert resp.create == True
        assert resp.read == True
        assert resp.update == True
        assert resp.delete == True

    def test_get_all_max_records(self):
        self.insert_manually.feature(session=self.session)

        data = ListFeatureServiceRequestDTO(max_records=1)

        resp = self.repo.get_all(data=data)

        assert len(resp) == 1

    def test_get_all_paper_id(self):
        inserted_feature = self.insert_manually.feature(session=self.session)

        data = ListFeatureServiceRequestDTO(paper_id=inserted_feature.paper_id)

        resp = self.repo.get_all(data=data)

        assert resp[0].paper_id == inserted_feature.paper_id
        assert len(resp) == 1

    def test_get_all_function_id(self):
        inserted_feature = self.insert_manually.feature(session=self.session)

        data = ListFeatureServiceRequestDTO(function_id=inserted_feature.function_id)

        resp = self.repo.get_all(data=data)

        assert resp[0].function_id == inserted_feature.function_id
        assert len(resp) == 1
