from typing import Optional
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Admin.Domain.Entities.UserAddress import UserAddress
from Shared.Domain.Entities.EntityBase import AggregateRootBase
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject
from Admin.Domain.Events.UserCreatedDomainEvent import UserCreatedDomainEvent
from Admin.Domain.Events.UserAddressAdded import UserAddressAdded
from Admin.Domain.Events.UserAddressRemoved import UserAddressRemoved


class User(AggregateRootBase):
    
    def __init__(
        self,
        username: UsernameValueObject,
        email: EmailValueObject,
        id: UuidValueObject,
        addresses: list[UserAddress] = None,
    ):
        super().__init__()
        
        self.id = id
        self.username = username
        self.email = email
        self._addresses: list[UserAddress] = addresses or []
        
    @staticmethod
    def create(
        username: str,
        email: str,
        id: str = None,
    ) -> 'User':
        
        return User(
            username=UsernameValueObject.create(username),
            email=EmailValueObject.create(email),
            id=UuidValueObject.create(id),
        )
    
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
        """Crea el evento de dominio y lo registra."""
        event = UserCreatedDomainEvent(
            user_id=self.id.value,
            username=self.username.value,
            email=self.email.value,
        )
        self.record_event(event)
