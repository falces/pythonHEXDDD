from Shared.Domain.Exceptions.IncorrectValueException import IncorrectValueException


class IncorrectEmailException(IncorrectValueException):
    def __init__(
        self,
        value: any,
    ):
        super().__init__(
            value = value,
            message = "Incorrect email: " + str(value),
        )