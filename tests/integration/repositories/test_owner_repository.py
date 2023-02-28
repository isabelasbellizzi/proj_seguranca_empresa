""" from dotenv import load_dotenv
import pytest
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.orm.execute_mapping import execute_mapping
from src.infra.repositories.implementations import OwnerRepository
from tests.integration.repositories import RepositoryBase,InsertManually
from src.services.DTOs.owner import \
    ListOwnerServiceRequestDTO
from src.domain.entities import Owner

class TestOwnerRepository (RepositoryBase):
    def setup_class(self) -> None:
        load_dotenv()
        execute_mapping()
        self.db = DbHandler(DbConfig())
        self.db.open()
        self.session = self.db.get_session()
        self.repo = OwnerRepository(self.db)
        self.insert_manually = InsertManually()


    def test_get_not_found(self) -> None:
        owner_id = -1
        resp = self.repo.get(id=owner_id)
        assert resp is None

    def test_get_found(self) -> None:
        inserted_paper = self.insert_manually.paper(session=self.session)# type: ignore
        paper_id = inserted_paper.paper_id

        # act
        resp = self.repo.get(paper_id=paper_id)

        # assert
        assert resp.paper_id == inserted_paper.paper_id# type: ignore
        assert resp.name == inserted_paper.name# type: ignore
        assert resp.system_id == inserted_paper.system_id# type: ignore
        assert resp.status == inserted_paper.status# type: ignore

    def test_get_all_max_records(self):
        self.insert_manually.paper(session=self.session) # type: ignore

        data = ListPaperServiceRequestDTO(max_records=1)
        # act
        resp = self.repo.get_all(data=data)
        # assert
        assert len(resp) == 1

    def test_get_all_system_id(self):
        inserted_manually = self.insert_manually.paper(session=self.session) # type: ignore

        data = ListPaperServiceRequestDTO(system_id=inserted_manually.system_id)
        # act
        resp = self.repo.get_all(data=data)

        # assert
        assert resp[0].system_id == inserted_manually.system_id
        assert len(resp) == 1

    def test_get_all_name(self):
        inserted_manually = self.insert_manually.paper(session=self.session) # type: ignore

        data = ListPaperServiceRequestDTO(paper_name=inserted_manually.name)
        # act
        resp = self.repo.get_all(data=data)
        # assert
        assert resp[0].name == inserted_manually.name
        assert len(resp) == 1

    def test_get_all_status(self):
        inserted_manually = self.insert_manually.paper(session=self.session) # type: ignore

        data = ListPaperServiceRequestDTO(paper_status=inserted_manually.status)
        # act
        resp = self.repo.get_all(data=data)
        # assert
        assert resp[0].status == inserted_manually.status

    def test_add_ok(self) -> None:
        inserted_paper = self.insert_manually.paper(session=self.session) # type: ignore

        new_paper = Paper(system_id=inserted_paper.system_id, name="papertest")
        # act
        self.repo.add(new_paper=new_paper)
        resp = self.repo.get(paper_id=new_paper.paper_id)
        # assert
        assert resp.paper_id != 0 or None # type: ignore
        assert resp.system_id == inserted_paper.system_id # type: ignore
        assert resp.name == "papertest" # type: ignore
        assert resp.status == 1 # type: ignore

    def test_delete_not_found_error(self) -> None:

        paper_id=1234
        with pytest.raises(Exception) as error:
            self.repo.delete(paper_id=paper_id)

        assert str(error.value) == f"Paper not found. [paper_id={paper_id}]"

    def test_delete_found(self) -> None:
        inserted_paper = self.insert_manually.paper(session=self.session) # type: ignore
        # act
        self.repo.delete(paper_id=inserted_paper.paper_id)
        # assert
        assert self.repo.get(paper_id=inserted_paper.paper_id) is None

    def test_update(self) -> None:
        inserted_paper = self.insert_manually.paper(session=self.session) # type: ignore

        paper = self.repo.get(paper_id=inserted_paper.paper_id)

        paper.name = "updated_name" # type: ignore
        self.repo.update(paper) # type: ignore

        resp = self.repo.get(paper_id=inserted_paper.paper_id)
        # assert
        assert resp.name == "updated_name" # type: ignore
         """