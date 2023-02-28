import os
from unittest import mock
import pytest
from src.infra.adaptors.db_config.db_config import DbConfig


class TestDbConfig:
    @pytest.mark.parametrize(
        ('env_variables', 'msg_erro'), (
            ({'DB_HOST': ''}, "Invalid database host"),
            ({'DB_HOST': 'pstgs-academy.postgres.database.azure.com', 'DB_NAME': ''}, "Invalid database name"),
            ({'DB_HOST': 'pstgs-academy.postgres.database.azure.com', 'DB_NAME': 'postgres', 'DB_USER': ''}, "Invalid database user"),
            ({'DB_HOST': 'pstgs-academy.postgres.database.azure.com', 'DB_NAME': 'postgres', 'DB_USER': 'academy_adm', 'DB_PASS': ''}, "Invalid database password"),
            ({'DB_HOST': 'pstgs-academy.postgres.database.azure.com', 'DB_NAME': 'postgres', 'DB_USER': 'academy_adm', 'DB_PASS': 'cJxRzPCsF9rcx', 'DB_DRIVER': ''}, "Invalid database driver"),
        )
    )
    def test_instance_error(self, env_variables: dict, msg_erro: str):
        with mock.patch.dict(os.environ, env_variables):
            with pytest.raises(Exception) as erro:
                _ = DbConfig()

            assert str(erro.value) == msg_erro

    @mock.patch.dict(os.environ, {'DB_HOST': 'host', 'DB_NAME': 'database', 'DB_USER': 'user', 'DB_PASS': 'password', 'DB_DRIVER': 'driver', 'DB_PORT': 'port'})
    def test_instance_ok(self):

        #act
        db_config = DbConfig()

        #assert
        assert db_config.host == 'host'
        assert db_config.database == 'database'
        assert db_config.user == 'user'
        assert db_config.passwd == 'password'
        assert db_config.driver == 'driver'
        assert db_config.port == 'port'
