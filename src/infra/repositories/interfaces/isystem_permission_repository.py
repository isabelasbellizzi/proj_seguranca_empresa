from abc import ABC, abstractmethod

class ISystemPermissionRepository(ABC):
    @abstractmethod
    def get_all(self, system_id: int):  # -> o que colocar como retorno?
        raise Exception("Not implemented")
