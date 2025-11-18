"""
Query para buscar HelloWorld con criterios específicos.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SearchHelloWorldQuery:
    """
    Query inmutable para buscar HelloWorld con filtros.
    
    Attributes:
        search_text: Texto a buscar en el greeting (opcional)
        limit: Número máximo de resultados (opcional)
        offset: Desplazamiento para paginación (opcional)
    """
    search_text: Optional[str] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0
    
    def __post_init__(self):
        """Validaciones básicas."""
        if self.limit is not None and (not isinstance(self.limit, int) or self.limit <= 0):
            raise ValueError("limit must be a positive integer")
        if self.offset is not None and (not isinstance(self.offset, int) or self.offset < 0):
            raise ValueError("offset must be a non-negative integer")
