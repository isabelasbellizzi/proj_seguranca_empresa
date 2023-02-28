from typing import Any
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler

class DbHandlerFake(IDbHandler):
    def __enter__(self):
        pass

    def get_session(self) -> Any:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def commit(self) -> None:
        pass

class TestServiceBase:
    db_handler = DbHandlerFake()
