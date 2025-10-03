class IntValueObject:
    def __init__(
        self,
        value: int,
    ):
        self.value = value
        
    def getValue(self) -> int:
        return self.value