from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import User


class IUserRepository(ABC):

    @abstractmethod
    def get_by_email(self, user_email: str) -> Optional[User]:
        raise Exception("Not implemented")

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[User]:
        raise Exception("Not implemented")

    @abstractmethod
    def get_all(self, max_records=0) -> List[User]:
        raise Exception("Not implemented")

    @abstractmethod
    def add(self, new: User) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def delete(self, user_id: int) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def update(self, obj: User) -> None:
        raise Exception("Not implemented")
