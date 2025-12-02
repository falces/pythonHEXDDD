class UserReadModel:
    
    def __init__(
        self,
        id: str,
        username: str,
        email: str,
    ):
        self.id = id
        self.username = username
        self.email = email
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'UserReadModel':
        return UserReadModel(
            id=data["id"],
            username=data["username"],
            email=data["email"],
        )