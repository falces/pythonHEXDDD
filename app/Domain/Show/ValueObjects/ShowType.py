from Shared.Domain.ValueObjects.StringValueObject import StringValueObject
from Shared.Domain.Exceptions.IncorrectValueException import IncorrectValueException
from typing import Self


class ShowType(StringValueObject):
    """
    Value Object para el tipo de Show (movie, series, etc).
    """
    
    VALID_TYPES = ['movie', 'series']
    
    def __init__(self, value: str):
        if not value:
            raise IncorrectValueException("ShowType cannot be empty")
        
        if value.lower() not in self.VALID_TYPES:
            raise IncorrectValueException(
                f"ShowType must be one of: {', '.join(self.VALID_TYPES)}"
            )
        
        super().__init__(value=value.lower())

    @staticmethod
    def create(value: str) -> Self:
        return ShowType(value)
    
    def isMovie(self) -> bool:
        return self.value == 'movie'
    
    def isSeries(self) -> bool:
        return self.value == 'series'
