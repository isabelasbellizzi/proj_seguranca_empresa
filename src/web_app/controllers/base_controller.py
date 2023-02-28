from src.infra.adaptors.db_config.db_config import DbConfig
from src.infra.adaptors.db_adapter.db_handler import DbHandler


class BaseRoute:
    def __init__(self) -> None:
        db_config = DbConfig()
        self.db_handler = DbHandler(db_config)
        self.db_handler.open()

    def __del__(self):
        self.db_handler.close()
