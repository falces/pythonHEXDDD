from dataclasses import dataclass


@dataclass(frozen=True)
class AddUserAddressCommand:
    """Comando para añadir una dirección a un usuario."""
    
    user_id: str
    street: str
    city: str
    country: str
