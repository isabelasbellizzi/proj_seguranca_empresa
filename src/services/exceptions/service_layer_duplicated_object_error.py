class ServiceLayerDuplicatedObjectError(Exception):

    @staticmethod
    def when(condicao: bool, mensagem: str) -> None:
        if condicao:
            raise ServiceLayerDuplicatedObjectError(mensagem)
