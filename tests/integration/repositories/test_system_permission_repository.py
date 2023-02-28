from typing import List
from dotenv import load_dotenv

from src.domain.entities import System, Paper, User
from src.infra.adaptors.db_adapter.db_handler import DbHandler
from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.orm.execute_mapping import execute_mapping
from src.infra.repositories.implementations import SystemPermissionRepository
from tests.integration.repositories import RepositoryBase, InsertManually


class TestSystemPermissionRepository(RepositoryBase):
    def setup_class(self) -> None:
        load_dotenv()
        execute_mapping()
        self.db = DbHandler(DbConfig())
        self.db.open()
        self.session = self.db.get_session()
        self.repo = SystemPermissionRepository(self.db)
        self.insert_manually = InsertManually()

    def test_get_all_ok(self) -> None:
        inserted_system: System = self.insert_manually.system(session=self.session)  # type: ignore
        system_id = inserted_system.system_id

        inserted_user: User = self.insert_manually.user(session=self.session)  # type: ignore
        user_id = inserted_user.user_id

        paper_sql_cmd = "INSERT INTO tb_paper (id, name, system_id, status) VALUES "
        paper_sql_cmd += f"(nextval('tb_paper_id_seq'), 'paper_name', '{system_id}', 1)"
        paper_sql_cmd += " RETURNING id as paper_id, name, system_id, status"
        inserted_paper: Paper = self.session.execute(paper_sql_cmd).first()  # type: ignore
        self.session.flush()  # type: ignore
        paper_id = inserted_paper.paper_id

        sql_cmd = "INSERT INTO tb_user_permissions (id, user_id, paper_id, status) VALUES "
        sql_cmd += f"(nextval('tb_user_permissions_id_seq'), {user_id}, '{paper_id}', 1)"
        sql_cmd += " RETURNING id as user_permission_id, user_id, paper_id, status"
        self.session.execute(sql_cmd).first()  # type: ignore
        self.session.flush()  # type: ignore

        # act
        resp = self.repo.get_all(system_id=system_id)

        # assert
        assert len(resp) == 1
        assert resp[0].user_id == user_id  # type: ignore
        assert resp[0].user_email == inserted_user.user_email  # type: ignore
        assert resp[0].paper_id == paper_id  # type: ignore
        assert resp[0].paper_name == inserted_paper.name  # type: ignore
