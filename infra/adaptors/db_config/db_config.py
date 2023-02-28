import os
from dataclasses import dataclass
from .idb_config import IDbConfig
from .exceptions.infra_dbconfig_error import InfraDbConfigError
from urllib.parse import quote  

@dataclass
class DbConfig(IDbConfig):

    def connect_string(self) -> str:
        return f"{self.driver}://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.database}"

    def __init__(self):
        self.host = os.environ.get('DB_HOST', "")
        InfraDbConfigError.when(not self.host, "Invalid database host")

        self.database = os.environ.get('DB_NAME', "")
        InfraDbConfigError.when(not self.database, "Invalid database name")

        self.user = os.environ.get('DB_USER', "")
        InfraDbConfigError.when(not self.user, "Invalid database user")

        self.passwd = quote(os.environ.get('DB_PASS', ""))
        InfraDbConfigError.when(not self.passwd, "Invalid database password")

        self.driver = os.environ.get('DB_DRIVER', "")
        InfraDbConfigError.when(not self.driver, "Invalid database driver")

        self.port = os.environ.get('DB_PORT', "")
        InfraDbConfigError.when(not self.port, "Invalid database port")

        self.debug = os.environ.get('DB_DEBUG', 'FALSE')

    @property
    def is_debug(self) -> bool:
        return self.debug.upper() == "TRUE"
