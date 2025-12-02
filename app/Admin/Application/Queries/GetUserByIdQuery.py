class GetUserByIdQuery:
    
    def __init__(
        self,
        id: str,
    ):
        self.id = id
    
    def __post_init__(self):
        if not isinstance(self.id, str) or self.id != 36:
            raise ValueError("Uuid not valid")
