from Shared.Domain.ValueObjects.StringValueObject import StringValueObject
from Shared.Domain.Exceptions.IncorrectValueException import IncorrectValueException
from typing import Self


class ShowId(StringValueObject):
    """
    Value Object para el identificador de un Show.
    """
    
    def __init__(self, value: str):
        if not value or len(value) == 0:
            raise IncorrectValueException("ShowId cannot be empty")
        
        super().__init__(value=value)

    @staticmethod
    def create(value: str) -> Self:
        return ShowId(value)
