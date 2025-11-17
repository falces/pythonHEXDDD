from abc import ABC
from datetime import datetime
from typing import Dict, Any
import uuid


class DomainEvent(ABC):
    """
    Clase base para todos los eventos de dominio.
    
    Los eventos de dominio representan algo que ha ocurrido en el pasado
    dentro del dominio y que es relevante para el negocio.
    
    Características:
    - Inmutables (una vez creados, no se modifican)
    - Nombrados en pasado (UserCreated, OrderPlaced, etc.)
    - Contienen toda la información necesaria para que los handlers actúen
    """
    
    def __init__(self):
        self._event_id: str = str(uuid.uuid4())
        self._occurred_on: datetime = datetime.now()
    
    @property
    def event_id(self) -> str:
        """Identificador único del evento."""
        return self._event_id
    
    @property
    def occurred_on(self) -> datetime:
        """Momento en que ocurrió el evento."""
        return self._occurred_on
    
    @property
    def event_name(self) -> str:
        """Nombre del evento (nombre de la clase)."""
        return self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serializa el evento a un diccionario.
        Las subclases deben sobrescribir este método para incluir datos específicos.
        """
        return {
            'event_id': self.event_id,
            'event_name': self.event_name,
            'occurred_on': self.occurred_on.isoformat(),
        }
    
    def __repr__(self) -> str:
        return f"{self.event_name}(event_id={self.event_id}, occurred_on={self.occurred_on})"
