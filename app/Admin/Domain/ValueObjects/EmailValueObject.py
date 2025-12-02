from typing import Self
from Shared.Domain.ValueObjects.StringValueObject import StringValueObject
from Admin.Domain.Exceptions.IncorrectEmailException import IncorrectEmailException


class EmailValueObject(StringValueObject):
    def __init__(
        self,
        value: str,
    ):
        super().__init__(value)
        
        trimmed_value = value.strip()

        if len(trimmed_value) < 1 or len(trimmed_value) > 255:
            raise IncorrectEmailException(value)
    
    @staticmethod
    def create(
        value: str,
    ) -> Self:
        return EmailValueObject(value)