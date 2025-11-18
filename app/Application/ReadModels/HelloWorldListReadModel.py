"""
Read Model para lista paginada de HelloWorld.
"""

from dataclasses import dataclass
from typing import List
from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel


@dataclass
class HelloWorldListReadModel:
    """
    Modelo de lectura para lista paginada de HelloWorld.
    Incluye metadata de paginación.
    
    Attributes:
        items: Lista de HelloWorldReadModel
        total: Total de items disponibles
        limit: Límite aplicado
        offset: Offset aplicado
    """
    items: List[HelloWorldReadModel]
    total: int
    limit: int
    offset: int
    
    @property
    def has_next(self) -> bool:
        """Indica si hay más páginas."""
        return (self.offset + self.limit) < self.total
    
    @property
    def has_previous(self) -> bool:
        """Indica si hay páginas anteriores."""
        return self.offset > 0
    
    def to_dict(self) -> dict:
        """
        Convierte a diccionario para serialización.
        
        Returns:
            dict: Representación con metadata de paginación
        """
        return {
            'items': [item.to_dict() for item in self.items],
            'total': self.total,
            'limit': self.limit,
            'offset': self.offset,
            'has_next': self.has_next,
            'has_previous': self.has_previous
        }
