import pytest
from dotenv import load_dotenv
from src.domain.entities import Function
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.orm.execute_mapping import execute_mapping
from src.infra.repositories.implementations import FunctionRepository
from src.services.DTOs.function.list_function_service_request_dto import ListFunctionServiceRequestDTO
from tests.integration.repositories import RepositoryBase, InsertManually

class TestFunctionRepository(RepositoryBase):
    def setup_class(self) -> None:
        load_dotenv()
        execute_mapping()
        self.db = DbHandler(DbConfig())
        self.db.open()
        self.session = self.db.get_session()
        self.repo = FunctionRepository(self.db)
        self.insert_manually = InsertManually()

    def test_Aget_not_found(self) -> None:
        function_id = -1

        resp = self.repo.get(id=function_id)

        assert resp == None

    def test_Bget_found(self) -> None:
        inserted_function = self.insert_manually.function(session=self.session)
        function_id = inserted_function.function_id

        # act
        resp = self.repo.get(id=function_id)

        # assert
        assert resp.function_id == inserted_function.function_id
        assert resp.system_id == inserted_function.system_id
        assert resp.name == inserted_function.name
        assert resp.function_type == inserted_function.function_type
        assert resp.status == inserted_function.status

    def test_Cget_by_name_not_found(self) -> None:
        function_name = "abc"

        resp = self.repo.get_byname(name=function_name)

        assert resp == None

    def test_Dget_by_name_found(self) -> None:
        inserted_function = self.insert_manually.function(session=self.session)
        function_name = inserted_function.name

        # act
        resp = self.repo.get_byname(name=function_name)

        # assert
        assert resp.function_id == inserted_function.function_id
        assert resp.system_id == inserted_function.system_id
        assert resp.name == inserted_function.name
        assert resp.function_type == inserted_function.function_type
        assert resp.status == inserted_function.status

    def test_Eget_by_name_id_exc_not_found(self) -> None:
        inserted_function = self.insert_manually.function(session=self.session)
        function_name = inserted_function.name
        function_id = inserted_function.function_id

        # act
        resp = self.repo.get_byname(name=function_name, id_exc=function_id)

        # assert
        assert resp == None

    def test_Fadd_ok(self) -> None:
        inserted_system = self.insert_manually.system(session=self.session)

        new_function = Function(system_id=inserted_system.system_id, name="function_name")

        self.repo.add(new_function=new_function)
        resp = self.repo.get(id=new_function.function_id)

        assert resp.function_id != 0 or None
        assert resp.system_id == inserted_system.system_id
        assert resp.name == "function_name"
        assert resp.function_type == 1
        assert resp.status == 1

    def test_Gdelete_not_found(self) -> None:
        with pytest.raises(Exception) as error:
            self.repo.delete(id=1234)

        assert str(error.value) == "Function not found. [function_id=1234]"

    def test_Hdelete_found(self) -> None:
        inserted_function = self.insert_manually.function(session=self.session)

        self.repo.delete(id=inserted_function.function_id)

        assert self.repo.get(id=inserted_function.function_id) is None

    def test_Iupdate(self) -> None:
        inserted_function = self.insert_manually.function(session=self.session)

        function = self.repo.get(id=inserted_function.function_id)

        function.name = "updated_name"
        function.function_type = 2

        self.repo.update(function=function)

        resp = self.repo.get(id=inserted_function.function_id)

        assert resp.name == "updated_name"
        assert resp.function_type == 2

    def test_Jget_all_max_records(self):
        self.insert_manually.function(session=self.session)

        data = ListFunctionServiceRequestDTO(max_records=1)

        resp = self.repo.get_all(data=data)

        assert len(resp) == 1

    def test_Kget_all_system_id(self):
        inserted_function = self.insert_manually.function(session=self.session)

        data = ListFunctionServiceRequestDTO(system_id=inserted_function.system_id)

        resp = self.repo.get_all(data=data)

        assert resp[0].system_id == inserted_function.system_id
        assert len(resp) == 1

    def test_Lget_all_function_name(self):
        inserted_function = self.insert_manually.function(session=self.session)

        data = ListFunctionServiceRequestDTO(function_name=inserted_function.name)

        resp = self.repo.get_all(data=data)

        assert resp[0].name == inserted_function.name
        assert len(resp) == 1

    def test_Mget_all_function_type(self):
        inserted_function = self.insert_manually.function(session=self.session)

        data = ListFunctionServiceRequestDTO(function_type=inserted_function.function_type)

        resp = self.repo.get_all(data=data)

        assert resp[0].function_type == inserted_function.function_type
