from Shared.Domain.ValueObjects.ValueObject import ValueObject


class StringValueObject(ValueObject):
    def __init__(
        self,
        value: str,
    ):
        super().__init__(value)