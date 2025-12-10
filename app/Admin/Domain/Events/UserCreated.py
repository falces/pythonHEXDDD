from typing import Any, Dict
from Shared.Domain.Events.DomainEvent import DomainEvent


class UserCreated(DomainEvent):
    
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__()
        self._user_id = user_id
        self._username = username
        self._email = email
        
    @property
    def id(self) -> str:
        return self._user_id
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def email(self) -> str:
        return self._email
    
    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            'id': self.id,
            'username': self.username,
            'email': self.email,
        })
        return base_dict
    
    def __repr__(self) -> str:
        return f"UserCreated(id={self.id}, username={self.username}, email={self.email})"