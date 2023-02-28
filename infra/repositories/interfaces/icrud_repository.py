from abc import ABC, abstractmethod
from typing import Any, List


class ICrudRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Any:
        raise Exception("Not Implemented")

    @abstractmethod
    def get_all(self) -> List[Any]:
        raise Exception("Not Implemented")

    @abstractmethod
    def add(self, new_object) -> None:
        raise Exception("Not Implemented")

    @abstractmethod
    def delete(self, id: int) -> None:
        raise Exception("Not Implemented")

    @abstractmethod
    def update(self, updated_object) -> None:
        raise Exception("Not Implemented")
