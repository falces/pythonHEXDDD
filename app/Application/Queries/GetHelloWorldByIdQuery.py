"""
Query para obtener un HelloWorld por su ID.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GetHelloWorldByIdQuery:
    """
    Query inmutable para obtener un HelloWorld específico.
    
    Attributes:
        id: ID del HelloWorld a buscar
    """
    id: int
    
    def __post_init__(self):
        """Validaciones básicas."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id must be a positive integer")
