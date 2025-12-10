from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteUserCommand:
    """Comando para eliminar un usuario."""
    
    id: str
