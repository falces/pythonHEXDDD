from Shared.Domain.ValueObjects.StringValueObject import StringValueObject
from Domain.HelloWorld.Exceptions.IncorrectGreetingException import IncorrectGreetingException
from typing import Self

class Greeting(StringValueObject):
    def __init__(
        self,
        value:str,
    ):
        if len(value) < 1 & len(value) > 255:
            raise IncorrectGreetingException(value)
        
        super().__init__(value = value)

    @staticmethod
    def create(
        value: str,
    ) -> Self:
        return Greeting(value)