from dotenv import load_dotenv
import pytest
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.orm.execute_mapping import execute_mapping
from src.infra.repositories.implementations import SystemRepository
from tests.integration.repositories import RepositoryBase,InsertManually
from src.services.DTOs.system.list_system_service_request_dto import \
    ListSystemServiceRequestDTO
from src.domain.entities import System

class TestSystemRepository (RepositoryBase):
    def setup_class(self) -> None:
        load_dotenv()
        execute_mapping()
        self.db = DbHandler(DbConfig())
        self.db.open()
        self.session = self.db.get_session()
        self.repo = SystemRepository(self.db)
        self.insert_manually = InsertManually()


    def test_get_byname_not_found(self) -> None:
        system_name = ""
        resp = self.repo.get_byname(system_name=system_name)
        assert resp is None

    def test_get_byname_found(self) -> None:
        inserted_system = self.insert_manually.system(session=self.session) # type: ignore
        system_name = inserted_system.name

        # act
        resp = self.repo.get_byname(system_name=system_name)

        # assert
        assert resp.system_id == inserted_system.system_id # type: ignore
        assert resp.token_id == inserted_system.token_id # type: ignore
        assert resp.system_name == inserted_system.name # type: ignore
        assert resp.status == inserted_system.status  # type: ignore

    def test_get_not_found(self) -> None:
        system_id = -1
        resp = self.repo.get(system_id=system_id)
        assert resp is None

    def test_get_found(self) -> None:
        inserted_system = self.insert_manually.system(session=self.session)# type: ignore
        system_id = inserted_system.system_id

        # act
        resp = self.repo.get(system_id=system_id)

        # assert
        assert resp.system_id == inserted_system.system_id # type: ignore
        assert resp.token_id == inserted_system.token_id # type: ignore
        assert resp.system_name == inserted_system.name # type: ignore
        assert resp.status == inserted_system.status  # type: ignore

    def test_get_all_max_records(self):
        self.insert_manually.system(session=self.session) # type: ignore

        data = ListSystemServiceRequestDTO(max_records=1)
        # act
        resp = self.repo.get_all(data=data)
        # assert
        assert len(resp) == 1

    def test_get_all_name(self):
        inserted_manually = self.insert_manually.system(session=self.session) # type: ignore

        data = ListSystemServiceRequestDTO(system_name=inserted_manually.name)
        # act
        resp = self.repo.get_all(data=data)
        # assert
        assert resp[0].system_name == inserted_manually.name
        assert len(resp) == 1

    def test_get_all_status(self):
        inserted_manually = self.insert_manually.system(session=self.session) # type: ignore

        data = ListSystemServiceRequestDTO(system_status=inserted_manually.status)
        # act
        resp = self.repo.get_all(data=data)
        # assert
        assert resp[0].status == inserted_manually.status

    def test_add_ok(self) -> None:
        inserted_manually = self.insert_manually.system(session=self.session) # type: ignore

        new_system = System(system_id=inserted_manually.system_id,token_id=inserted_manually.token_id, system_name="papertest")

        # act
        self.repo.add(new=new_system)
        resp = self.repo.get(system_id=new_system.system_id)

        # assert
        assert resp.system_id != 0 or None # type: ignore
        assert resp.token_id == inserted_manually.token_id # type: ignore
        assert resp.system_name == "papertest" # type: ignore
        assert resp.status == 1 # type: ignore

    def test_delete_not_found(self) -> None:
        system_id=1234
        with pytest.raises(Exception) as error:
            self.repo.delete(system_id=system_id)

        assert str(error.value) == f"System not found. [system_id={system_id}]"

    def test_delete_found(self) -> None:
        inserted_manually = self.insert_manually.system(session=self.session) # type: ignore
        # act
        self.repo.delete(system_id=inserted_manually.system_id)
        # assert
        assert self.repo.get(system_id=inserted_manually.system_id) is None

    def test_update(self) -> None:
        inserted_manually = self.insert_manually.system(session=self.session) # type: ignore

        system = self.repo.get(system_id=inserted_manually.system_id)

        system.name = "updated_name" # type: ignore
        self.repo.update(system) # type: ignore

        resp = self.repo.get(system_id=inserted_manually.system_id)
        # assert
        assert resp.name == "updated_name" # type: ignore
