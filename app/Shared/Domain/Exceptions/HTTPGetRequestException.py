from Shared.Domain.Exceptions.ExceptionBase import ExceptionBase

class HTTPGetRequestException(ExceptionBase):

    MESSAGE = 'Error on GET HTTP Request: '

    def __init__(
        self,
        message: str,
        code: int
    ):
        super().__init__(
            self.MESSAGE + message,
            code,
        )