from Shared.Domain.ValueObjects.IntValueObject import IntValueObject
from Shared.Domain.Exceptions.IncorrectValueException import IncorrectValueException

class IdValueobject(IntValueObject):
    def __init__(
        self,
        value: int,
    ):
        if value < 0:
            raise IncorrectValueException(
                message = "Value " + str(value) + " is not valid for ID",
            )
        
        super().__init__(value)