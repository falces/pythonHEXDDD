"""
Evento de dominio: Dirección eliminada de usuario.
"""
from typing import Any, Dict
from Shared.Domain.Events.DomainEvent import DomainEvent


class UserAddressRemoved(DomainEvent):
    
    def __init__(self, user_id: str, address_id: str):
        super().__init__()
        self._user_id = user_id
        self._address_id = address_id
        
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def address_id(self) -> str:
        return self._address_id
    
    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            'user_id': self.user_id,
            'address_id': self.address_id,
        })
        return base_dict
    
    def __repr__(self) -> str:
        return f"UserAddressRemoved(user_id={self.user_id}, address_id={self.address_id})"
