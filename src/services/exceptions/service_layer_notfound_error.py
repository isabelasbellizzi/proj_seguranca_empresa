class ServiceLayerNotFoundError(Exception):

    @staticmethod
    def when(condicao: bool, mensagem: str) -> None:
        if condicao:
            raise ServiceLayerNotFoundError(mensagem)
