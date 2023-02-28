class ServiceLayerForeignKeyError(Exception):

    @staticmethod
    def when(condicao: bool, mensagem: str) -> None:
        if condicao:
            raise ServiceLayerForeignKeyError(mensagem)
