"""
Command para crear un nuevo HelloWorld.
Representa la intención de crear una entidad.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateHelloWorldCommand:
    """
    Comando inmutable para crear un HelloWorld.
    
    Attributes:
        greeting_text: Texto del saludo a crear
    """
    greeting_text: str
    
    def __post_init__(self):
        """Validaciones básicas del comando."""
        if not isinstance(self.greeting_text, str):
            raise TypeError("greeting_text must be a string")
