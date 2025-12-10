from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateUserCommand:
    """Comando para actualizar un usuario existente."""
    
    id: str
    username: str = None
    email: str = None
