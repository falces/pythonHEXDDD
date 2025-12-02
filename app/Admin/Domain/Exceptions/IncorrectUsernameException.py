from Shared.Domain.Exceptions.IncorrectValueException import IncorrectValueException


class IncorrectUsernameException(IncorrectValueException):
    def __init__(
        self,
        value: any,
    ):
        super().__init__(
            value = value,
            message = "Incorrect username: " + str(value),
        )