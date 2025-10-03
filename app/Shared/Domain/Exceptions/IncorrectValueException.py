from Shared.Domain.Exceptions.ExceptionBase import ExceptionBase

class IncorrectValueException(ExceptionBase):
    
    def __init__(
        self,
        value: any,
        code: int = 500,
        message = None,
    ):
        if message == None:
            message = f"Incorrect value: {value}"
        
        super().__init__(
            message = message,
            code = code,
        )