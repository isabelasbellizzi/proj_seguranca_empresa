import pytest
from dotenv import load_dotenv

from src.domain.entities import User
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.orm.execute_mapping import execute_mapping
from src.infra.repositories.implementations import UserRepository
from tests.integration.repositories import InsertManually, RepositoryBase


class TestUserRepository(RepositoryBase):
    def setup_class(self) -> None:
        load_dotenv()
        execute_mapping()

        self.db = DbHandler(DbConfig()) # pylint: disable=attribute-defined-outside-init
        self.db.open() # pylint: disable=attribute-defined-outside-init

        self.session = self.db.get_session() # pylint: disable=attribute-defined-outside-init
        self.repo = UserRepository(self.db) # pylint: disable=attribute-defined-outside-init
        self.insert_manually = InsertManually() # pylint: disable=attribute-defined-outside-init

    ###CREATE###

    def test_add_ok(self) -> None:
        # Arrange
        inserted_user = self.insert_manually.user(session=self.session) #type: ignore
        user_add = User(azure_id=inserted_user.azure_id, user_email=inserted_user.user_email, status=inserted_user.status)

        # Act
        self.repo.add(new=user_add)
        new_user = self.repo.get_by_user_id(user_id=user_add.user_id)

        # Assert
        assert new_user.user_id != 0 or None #type: ignore 
        assert new_user.azure_id == inserted_user.azure_id #type: ignore 
        assert new_user.user_email == inserted_user.user_email #type: ignore 
        assert new_user.status == 1 #type: ignore

    ###READ###
    def test_get_by_user_id_not_found_error(self) -> None:
        # Arrange
        test_id = -1

        # Act
        resp = self.repo.get_by_user_id(user_id=test_id)

        # Assert
        assert resp == None # pylint: disable=singleton-comparison


    def test_get_by_user_id_found_ok(self) -> None:
        # Arrange
        inserted_user = self.insert_manually.user(session=self.session) #type: ignore
        test_id = inserted_user.user_id

        # Act
        resp = self.repo.get_by_user_id(user_id=test_id)

        # Assert
        assert resp.user_id == inserted_user.user_id #type: ignore
        assert resp.azure_id == inserted_user.azure_id #type: ignore
        assert resp.user_email == inserted_user.user_email #type: ignore
        assert resp.status == inserted_user.status #type: ignore

    def test_get_by_user_email_error(self) -> None:
        # Arrange
        test_email = "teste"

        # Act
        resp = self.repo.get_by_email(user_email=test_email)

        # Assert
        assert resp == None # pylint: disable=singleton-comparison

    def test_get_by_user_email_ok(self) -> None:
        # Arrange
        inserted_user = self.insert_manually.user(session=self.session) #type: ignore
        test_email = inserted_user.user_email

        # Act
        resp = self.repo.get_by_email(user_email=test_email)

        # Assert
        assert resp.user_id == inserted_user.user_id #type: ignore
        assert resp.azure_id == inserted_user.azure_id #type: ignore
        assert resp.user_email == inserted_user.user_email #type: ignore
        assert resp.status == inserted_user.status #type: ignore

    def test_get_all_max_records_ok(self):
        # Arrange
        max_records = 1

        # Act
        resp = self.repo.get_all(max_records= 1)

        # Assert
        assert len(resp) == max_records

    ###UPDATE###

    def test_update_ok(self) -> None:
        # Arrange
        inserted_user = self.insert_manually.user(session=self.session) #type: ignore

        # Act
        update = self.repo.get_by_user_id(user_id=inserted_user.user_id)
        update.user_email = "teste2@test.com" #type: ignore

        self.repo.update(obj=update) #type: ignore

        resp = self.repo.get_by_user_id(user_id=inserted_user.user_id)

        # Assert
        assert resp.user_email == "teste2@test.com" #type: ignore

    ###DELETE###

    def test_delete_found_ok(self) -> None:
        # Arrange
        inserted_user = self.insert_manually.user(session=self.session) #type: ignore

        # Act
        self.repo.delete(user_id=inserted_user.user_id)

        # Assert
        assert self.repo.get_by_user_id(user_id=inserted_user.user_id) is None

    def test_delete_not_found_error(self) -> None:

        with pytest.raises(Exception) as error:
            self.repo.delete(user_id=1234)

        assert str(error.value) == "User not found. [user_id=1234]"
