from Shared.Domain.ValueObjects.StringValueObject import StringValueObject
from Shared.Domain.Exceptions.IncorrectValueException import IncorrectValueException
from typing import Self


class ShowTitle(StringValueObject):
    """
    Value Object para el título de un Show.
    """
    
    def __init__(self, value: str):
        if not value or len(value) == 0:
            raise IncorrectValueException("ShowTitle cannot be empty")
        
        if len(value) > 500:
            raise IncorrectValueException("ShowTitle cannot exceed 500 characters")
        
        super().__init__(value=value)

    @staticmethod
    def create(value: str) -> Self:
        return ShowTitle(value)
