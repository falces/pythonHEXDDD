from Shared.Domain.Exceptions.ExceptionBase import ExceptionBase


class DatabaseException(ExceptionBase):
    def __init__(
        self,
        message: str = None,
        code: int = 500,
    ):
        if message is None:
            message = "Database error occurred"
        super().__init__(message, code)