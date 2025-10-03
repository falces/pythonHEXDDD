class StringValueObject():
    def __init__(
        self,
        value:str
    ):
        self.value = value
    
    def getValue(self) -> str:
        return self.value