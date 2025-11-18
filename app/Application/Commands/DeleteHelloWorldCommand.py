"""
Command para eliminar un HelloWorld.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteHelloWorldCommand:
    """
    Comando inmutable para eliminar un HelloWorld.
    
    Attributes:
        id: ID del HelloWorld a eliminar
    """
    id: int
    
    def __post_init__(self):
        """Validaciones básicas del comando."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id must be a positive integer")
