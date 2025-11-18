"""
Read Model optimizado para consultas de HelloWorld.
Sin lógica de dominio, solo datos para lectura.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class HelloWorldReadModel:
    """
    Modelo de lectura para HelloWorld.
    Optimizado para queries, sin comportamiento de dominio.
    
    Attributes:
        id: Identificador único
        greeting: Texto del saludo
        created_at: Fecha de creación (opcional)
        updated_at: Fecha de última actualización (opcional)
    """
    id: int
    greeting: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """
        Convierte el read model a diccionario para serialización.
        
        Returns:
            dict: Representación en diccionario
        """
        result = {
            'id': self.id,
            'greeting': self.greeting
        }
        
        if self.created_at:
            result['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            result['updated_at'] = self.updated_at.isoformat()
            
        return result
    
    @staticmethod
    def from_dict(data: dict) -> 'HelloWorldReadModel':
        """
        Crea un read model desde un diccionario.
        
        Args:
            data: Diccionario con los datos
            
        Returns:
            HelloWorldReadModel: Instancia creada
        """
        return HelloWorldReadModel(
            id=data['id'],
            greeting=data['greeting'],
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
