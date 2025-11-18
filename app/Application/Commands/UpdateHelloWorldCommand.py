"""
Command para actualizar un HelloWorld existente.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateHelloWorldCommand:
    """
    Comando inmutable para actualizar un HelloWorld.
    
    Attributes:
        id: ID del HelloWorld a actualizar
        greeting_text: Nuevo texto del saludo
    """
    id: int
    greeting_text: str
    
    def __post_init__(self):
        """Validaciones básicas del comando."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id must be a positive integer")
        if not isinstance(self.greeting_text, str):
            raise TypeError("greeting_text must be a string")
