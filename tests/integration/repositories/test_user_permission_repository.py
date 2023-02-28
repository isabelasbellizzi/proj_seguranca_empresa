import pytest
from dotenv import load_dotenv

from src.domain.entities import UserPermission
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.orm.execute_mapping import execute_mapping
from src.infra.repositories.implementations import UserPermissionRepository
from src.services.DTOs.user_permission import \
    ListUserPermissionServiceRequestDTO
from tests.integration.repositories import InsertManually, RepositoryBase


class TestUserPermissionRepository(RepositoryBase):
    def setup_class(self) -> None:
        load_dotenv()
        execute_mapping()

        self.db = DbHandler(DbConfig()) # pylint: disable=attribute-defined-outside-init
        self.db.open() # pylint: disable=attribute-defined-outside-init

        self.session = self.db.get_session() # pylint: disable=attribute-defined-outside-init
        self.repo = UserPermissionRepository(self.db) # pylint: disable=attribute-defined-outside-init
        self.insert_manually = InsertManually() # pylint: disable=attribute-defined-outside-init

    ###CREATE###

    def test_add_ok(self) -> None:
        # Arrange
        inserted_paper = self.insert_manually.paper(session=self.session) #type: ignore
        inserted_user = self.insert_manually.user(session=self.session) #type: ignore

        new_up = UserPermission(user_id=inserted_user.user_id, paper_id=inserted_paper.paper_id, status=1) #type: ignore 

        # Act
        self.repo.add(new_user_permission=new_up)

        # Assert
        assert new_up.user_id != 0 or None
        assert new_up.user_permission_id == new_up.user_permission_id
        assert new_up.paper_id == new_up.paper_id
        assert new_up.status == 1

    ###READ###
    def test_get_by_user_id_not_found_error(self) -> None:
        # Arrange
        test_id = -1

        # Act
        resp = self.repo.get(user_permission_id=test_id)

        # Assert
        assert resp == None # pylint: disable=singleton-comparison


    def test_get_by_user_id_found_ok(self) -> None:
        # Arrange
        inserted_up = self.insert_manually.user_permission(session=self.session) #type: ignore
        test_id = inserted_up.user_permission_id

        # Act
        resp = self.repo.get(user_permission_id=test_id)

        # Assert
        assert resp.user_permission_id == inserted_up.user_permission_id #type: ignore
        assert resp.user_id == inserted_up.user_id #type: ignore
        assert resp.paper_id == inserted_up.paper_id #type: ignore
        assert resp.status == inserted_up.status #type: ignore

    def test_get_all_max_records_ok(self):
        # Arrange
        data = ListUserPermissionServiceRequestDTO(max_records = 1)

        # Act
        resp = self.repo.get_all(data=data)

        # Assert
        assert len(resp) == 1

    ###UPDATE###

    def test_update_ok(self) -> None:
        # Arrange
        inserted_up = self.insert_manually.user_permission(session=self.session) #type: ignore

        # Act
        new_up = self.repo.get(user_permission_id=inserted_up.user_permission_id)
        new_up.status = 2 #type: ignore

        self.repo.update(user_permission=new_up) #type: ignore

        resp = self.repo.get(user_permission_id=inserted_up.user_permission_id)

        # Assert
        assert resp.status == 2 #type: ignore

    ###DELETE###

    def test_delete_found_ok(self) -> None:
        # Arrange
        inserted_up = self.insert_manually.user_permission(session=self.session) #type: ignore

        # Act
        self.repo.delete(user_permission_id=inserted_up.user_permission_id)

        # Assert
        assert self.repo.get(user_permission_id=inserted_up.user_permission_id) is None

    def test_delete_not_found_error(self) -> None:
        id = 1234

        with pytest.raises(Exception) as error:
            self.repo.delete(user_permission_id=id)

        assert str(error.value) == f"User Permission not found. [user_permission_id={id}]"
