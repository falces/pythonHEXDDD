"""
Entidad UserAddress - pertenece al agregado User.
"""
from typing import Self
import uuid
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class UserAddress:
    """
    Entidad que representa una dirección del usuario.
    Pertenece al agregado User (no es un Aggregate Root).
    """
    
    def __init__(
        self,
        street: str,
        city: str,
        country: str,
        id: UuidValueObject = None,
    ):
        self.id = id or UuidValueObject.create(str(uuid.uuid4()))
        self.street = street
        self.city = city
        self.country = country
    
    @staticmethod
    def create(
        street: str,
        city: str,
        country: str,
        id: UuidValueObject = None,
    ) -> Self:
        return UserAddress(
            street=street,
            city=city,
            country=country,
            id=id,
        )
    
    def update(self, street: str = None, city: str = None, country: str = None) -> None:
        """Actualiza los datos de la dirección."""
        if street:
            self.street = street
        if city:
            self.city = city
        if country:
            self.country = country
