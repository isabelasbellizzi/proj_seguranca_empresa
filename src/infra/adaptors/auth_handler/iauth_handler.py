from abc import ABC
from typing import Any

class IAuthHandler(ABC):
    @staticmethod
    def lista_configuracao() -> Any:
        raise Exception("Rotina não implementada")

    @staticmethod
    def authenticate(chave: str, senha: str) -> str:
        raise Exception("Rotina não implementada")
