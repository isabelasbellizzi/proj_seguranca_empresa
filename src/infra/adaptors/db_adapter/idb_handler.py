from abc import ABC
from dataclasses import dataclass
from typing import Any

@dataclass
class IDbHandler(ABC):
    def __enter__(self):
        raise Exception("Not Implemented")

    def get_session(self) -> Any:
        raise Exception("Not Implemented")

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise Exception("Not Implemented")

    def commit(self) -> None:
        raise Exception("Not Implemented")
