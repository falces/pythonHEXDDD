from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UpdateUserAddressCommand:
    """Comando para actualizar una dirección de un usuario."""
    
    user_id: str
    address_id: str
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
