from typing import Optional
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.adaptors.db_config.idb_config import IDbConfig
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler

class DbHandler (IDbHandler):
    def __init__(self, db_config: IDbConfig):
        self.session = None
        self.session_maker = None
        self.engine = None
        self.db_config = db_config

    def __enter__(self):
        path = self.db_config.connect_string()
        self.engine = create_engine(path, echo=self.db_config.is_debug)
        self.session_maker = sessionmaker()
        self.session = self.session_maker(bind=self.engine)
        return self

    def get_session(self) -> Optional[Session]:
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if (self.session):
            self.session.close()

    def commit(self) -> None:
        if (self.session):
            self.session.commit()

    def close(self) -> None:
        self.session.close()
        self.engine.dispose(close=True)

    def open(self) -> None:
        path = self.db_config.connect_string()
        self.engine = create_engine(path, echo=self.db_config.is_debug)
        self.session_maker = sessionmaker()
        self.session = self.session_maker(bind=self.engine)
