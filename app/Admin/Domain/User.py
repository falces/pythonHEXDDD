from typing import Self, Optional
import uuid
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Admin.Domain.Entities.UserAddress import UserAddress
from Shared.Domain.Entities.EntityBase import AggregateRootBase
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject
from Admin.Domain.Events.UserCreated import UserCreated
from Admin.Domain.Events.UserAddressAdded import UserAddressAdded
from Admin.Domain.Events.UserAddressRemoved import UserAddressRemoved


class User(AggregateRootBase):
    
    def __init__(
        self,
        username: UsernameValueObject,
        email: EmailValueObject,
        id: UuidValueObject = None,
        addresses: list[UserAddress] = None,
    ):
        super().__init__()
        
        if id is None:
            id = UuidValueObject.create(str(uuid.uuid4()))
        
        self.id = id
        self.username = username
        self.email = email
        self._addresses: list[UserAddress] = addresses or []
        
    @staticmethod
    def create(
        username: UsernameValueObject,
        email: EmailValueObject,
        id: UuidValueObject = None,
    ) -> Self:
        return User(
            username=username,
            email=email,
            id=id,
        )
    
    # --- Gestión de direcciones (entidad hija) ---
    
    @property
    def addresses(self) -> list[UserAddress]:
        """Devuelve una copia de las direcciones (inmutabilidad)."""
        return list(self._addresses)
    
    def add_address(self, street: str, city: str, country: str) -> UserAddress:
        """Añade una nueva dirección al usuario."""
        address = UserAddress.create(street=street, city=city, country=country)
        self._addresses.append(address)
        
        self.record_event(UserAddressAdded(
            user_id=self.id.value,
            address_id=address.id.value,
            street=street,
            city=city,
            country=country,
        ))
        
        return address
    
    def remove_address(self, address_id: UuidValueObject) -> bool:
        """Elimina una dirección del usuario."""
        for address in self._addresses:
            if address.id.value == address_id.value:
                self._addresses.remove(address)
                
                self.record_event(UserAddressRemoved(
                    user_id=self.id.value,
                    address_id=address_id.value,
                ))
                
                return True
        return False
    
    def get_address(self, address_id: UuidValueObject) -> Optional[UserAddress]:
        """Obtiene una dirección por su ID."""
        for address in self._addresses:
            if address.id.value == address_id.value:
                return address
        return None
        
    def mark_as_created(self) -> None:
        event = UserCreated(
            user_id=self.id.value,
            username=self.username.value,
            email=self.email.value,
        )
        self.record_event(event)
