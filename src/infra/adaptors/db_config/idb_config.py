from abc import ABC
from dataclasses import dataclass

@dataclass
class IDbConfig(ABC):
    def connect_string(self) -> str:
        raise Exception("Not implemented")

    @property
    def is_debug(self) -> bool:
        raise Exception("Not implemented")
