"""
Query para obtener todos los HelloWorld.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GetAllHelloWorldQuery:
    """
    Query inmutable para obtener todos los HelloWorld.
    
    Attributes:
        limit: Número máximo de resultados (opcional)
        offset: Desplazamiento para paginación (opcional)
        sort_by: Campo por el cual ordenar (opcional)
        sort_order: Orden ascendente o descendente (opcional)
    """
    limit: Optional[int] = None
    offset: Optional[int] = None
    sort_by: Optional[str] = 'id'
    sort_order: Optional[str] = 'asc'
    
    def __post_init__(self):
        """Validaciones básicas."""
        if self.limit is not None and (not isinstance(self.limit, int) or self.limit <= 0):
            raise ValueError("limit must be a positive integer")
        if self.offset is not None and (not isinstance(self.offset, int) or self.offset < 0):
            raise ValueError("offset must be a non-negative integer")
        if self.sort_order not in ['asc', 'desc', None]:
            raise ValueError("sort_order must be 'asc' or 'desc'")
