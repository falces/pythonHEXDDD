"""
Evento de dominio: Dirección añadida a usuario.
"""
from typing import Any, Dict
from Shared.Domain.Events.DomainEvent import DomainEvent


class UserAddressAdded(DomainEvent):
    
    def __init__(self, user_id: str, address_id: str, street: str, city: str, country: str):
        super().__init__()
        self._user_id = user_id
        self._address_id = address_id
        self._street = street
        self._city = city
        self._country = country
        
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def address_id(self) -> str:
        return self._address_id
    
    @property
    def street(self) -> str:
        return self._street
    
    @property
    def city(self) -> str:
        return self._city
    
    @property
    def country(self) -> str:
        return self._country
    
    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            'user_id': self.user_id,
            'address_id': self.address_id,
            'street': self.street,
            'city': self.city,
            'country': self.country,
        })
        return base_dict
    
    def __repr__(self) -> str:
        return f"UserAddressAdded(user_id={self.user_id}, address_id={self.address_id}, city={self.city})"
