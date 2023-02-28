class ServiceLayerDuplicatedNameError(Exception):

    @staticmethod
    def when(condicao: bool, mensagem: str) -> None:
        if condicao:
            raise ServiceLayerDuplicatedNameError(mensagem)
