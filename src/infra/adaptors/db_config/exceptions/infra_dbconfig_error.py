class InfraDbConfigError(Exception):

    @staticmethod
    def when(condition: bool, message: str) -> None:
        if condition:
            raise InfraDbConfigError(message)
