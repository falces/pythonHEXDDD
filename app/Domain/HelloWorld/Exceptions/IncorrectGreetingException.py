from Shared.Domain.Exceptions.IncorrectValueException import IncorrectValueException

class IncorrectGreetingException(IncorrectValueException):
    def __init__(
        self,
        value: any,
    ):
        super().__init__(
            value = value,
            message = "Incorrect greeting: " + str(value),
        )