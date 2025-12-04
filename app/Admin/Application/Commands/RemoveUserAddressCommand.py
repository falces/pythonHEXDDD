from dataclasses import dataclass


@dataclass(frozen=True)
class RemoveUserAddressCommand:
    """Comando para eliminar una dirección de un usuario."""
    
    user_id: str
    address_id: str
