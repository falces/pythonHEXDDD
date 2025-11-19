from Shared.Domain.ValueObjects.StringValueObject import StringValueObject
from Domain.HelloWorld.Exceptions.IncorrectGreetingException import IncorrectGreetingException
from typing import Self


class GreetingValueObject(StringValueObject):
    def __init__(
        self,
        value: str,
    ):
        # Trim whitespace
        trimmed_value = value.strip()

        # Validate length
        if len(trimmed_value) < 1 or len(trimmed_value) > 255:
            raise IncorrectGreetingException(value)

        super().__init__(value=trimmed_value)

    @staticmethod
    def create(
        value: str,
    ) -> Self:
        return GreetingValueObject(value)
