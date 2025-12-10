from typing import List, Optional


class UserReadModel:
    
    def __init__(
        self,
        id: str,
        username: str,
        email: str,
        addresses: Optional[List[dict]] = None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.addresses = addresses or []
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "addresses": self.addresses,
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'UserReadModel':
        return UserReadModel(
            id=data["id"],
            username=data["username"],
            email=data["email"],
            addresses=data.get("addresses", []),
        )