from dataclasses import dataclass
from typing import Any
from uuid import uuid4
from faker import Faker
from sqlalchemy.orm.session import Session


@dataclass
class InsertManually:
    faker = Faker()

    def system(self, session: Session) -> Any:
        name = 'system_name'
        token_id = uuid4()

        sql_cmd = "INSERT INTO tb_system (id, token_id, name, status) VALUES "
        sql_cmd += f"(nextval('tb_system_id_seq'),'{token_id}', '{name}',1)"
        sql_cmd += " RETURNING id as system_id, token_id, name, status"
        retorno = session.execute(sql_cmd).first()
        session.flush()

        return retorno

    def function(self, session: Session) -> Any:
        inserted_system = self.system(session=session)

        system_id = inserted_system.system_id
        name = 'function_name'

        sql_cmd = "INSERT INTO tb_function (id, system_id, name, function_type, status) VALUES "
        sql_cmd += f"(nextval('tb_function_id_seq'), {system_id}, '{name}', 1, 1)"
        sql_cmd += " RETURNING id as function_id, system_id, name, function_type, status"
        retorno = session.execute(sql_cmd).first()
        session.flush()

        return retorno

    def paper(self, session: Session) -> Any:
        inserted_system = self.system(session=session)

        system_id = inserted_system.system_id
        name = 'paperr_name'

        sql_cmd = "INSERT INTO tb_paper (id, name, system_id, status) VALUES "
        sql_cmd += f"(nextval('tb_paper_id_seq'), '{name}', '{system_id}', 1)"
        sql_cmd += " RETURNING id as paper_id, name, system_id, status"
        retorno = session.execute(sql_cmd).first()
        session.flush()

        return retorno

    def user(self, session: Session) -> Any:
        azure_id = uuid4()
        user_email = 'usuario@transfero.com'

        sql_cmd = "INSERT INTO tb_user (id, user_email, azure_id, status) VALUES "
        sql_cmd += f"(nextval('tb_user_id_seq'), '{user_email}', '{azure_id}', 1)"
        sql_cmd += " RETURNING id as user_id, user_email, azure_id, status"
        retorno = session.execute(sql_cmd).first()
        session.flush()

        return retorno

    def feature(self, session: Session) -> Any:
        inserted_paper = self.paper(session=session)
        inserted_function = self.function(session=session)

        paper_id = inserted_paper.paper_id
        function_id = inserted_function.function_id


        sql_cmd = "INSERT INTO tb_features (id, paper_id, function_id, allow_get, allow_insert, allow_update, allow_delete, status) VALUES "
        sql_cmd += f"(nextval('tb_features_id_seq'), {paper_id}, '{function_id}', false, false, false, false, 1)"
        sql_cmd += " RETURNING id as feature_id, paper_id, function_id, allow_get as read, allow_insert as create, allow_update as update, allow_delete as delete, status"
        retorno = session.execute(sql_cmd).first()
        session.flush()

        return retorno

    def user_permission(self, session: Session) -> Any:
        inserted_paper = self.paper(session=session)
        inserted_user = self.user(session=session)

        paper_id = inserted_paper.paper_id
        user_id = inserted_user.user_id


        sql_cmd = "INSERT INTO tb_user_permissions (id, user_id, paper_id, status) VALUES "
        sql_cmd += f"(nextval('tb_user_permissions_id_seq'), {user_id}, '{paper_id}', 1)"
        sql_cmd += " RETURNING id as user_permission_id, user_id, paper_id, status"
        retorno = session.execute(sql_cmd).first()
        session.flush()

        return retorno
