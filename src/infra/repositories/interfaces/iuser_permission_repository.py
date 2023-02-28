from abc import ABC, abstractmethod
from typing import Any, List

from src.domain.entities import UserPermission
from src.services.DTOs.user_permission import \
    ListUserPermissionServiceRequestDTO

class IUserPermissionRepository(ABC):

    @abstractmethod
    def get(self, user_permission_id: int) -> Any:
        raise Exception("Not implemented")

    @abstractmethod
    def get_all(self, data: ListUserPermissionServiceRequestDTO) -> List[Any]:
        raise Exception("Not implemented")

    @abstractmethod
    def add(self, new_user_permission: UserPermission) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def delete(self, user_permission_id: int) -> None:
        raise Exception("Not implemented")

    @abstractmethod
    def update(self, user_permission: UserPermission) -> None:
        raise Exception("Not implemented")
