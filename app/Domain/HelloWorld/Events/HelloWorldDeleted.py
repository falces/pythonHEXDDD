from typing import Dict, Any
from Shared.Domain.Events.DomainEvent import DomainEvent


class HelloWorldDeleted(DomainEvent):
    """
    Evento de dominio: Se ha eliminado un HelloWorld.
    
    Este evento se dispara cuando se elimina exitosamente un HelloWorld
    y puede ser usado para:
    - Logging/Auditoría
    - Limpieza de recursos relacionados
    - Notificaciones
    - Sincronización con otros sistemas
    """
    
    def __init__(self, hello_world_id: int):
        super().__init__()
        self._hello_world_id = hello_world_id
    
    @property
    def hello_world_id(self) -> int:
        """ID del HelloWorld eliminado."""
        return self._hello_world_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el evento con sus datos específicos."""
        base_dict = super().to_dict()
        base_dict.update({
            'hello_world_id': self.hello_world_id,
        })
        return base_dict
    
    def __repr__(self) -> str:
        return f"HelloWorldDeleted(id={self.hello_world_id})"
