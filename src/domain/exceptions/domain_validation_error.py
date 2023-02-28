class DomainValidationError(Exception):

    @staticmethod
    def when(condition: bool, message: str) -> None:
        if condition:
            raise DomainValidationError(message)
