from typing import Dict, Any
from Shared.Domain.Events.DomainEvent import DomainEvent


class HelloWorldUpdated(DomainEvent):
    """
    Evento de dominio: Se ha actualizado un HelloWorld.

    Este evento se dispara cuando se actualiza exitosamente un HelloWorld
    y puede ser usado para:
    - Logging/Auditoría
    - Notificaciones
    - Sincronización con otros sistemas
    - Analytics
    """

    def __init__(self, hello_world_id: int, greeting: str):
        super().__init__()
        self._hello_world_id = hello_world_id
        self._greeting = greeting

    @property
    def hello_world_id(self) -> int:
        """ID del HelloWorld actualizado."""
        return self._hello_world_id

    @property
    def greeting(self) -> str:
        """Texto del saludo."""
        return self._greeting

    def to_dict(self) -> Dict[str, Any]:
        """Serializa el evento con sus datos específicos."""
        base_dict = super().to_dict()
        base_dict.update({
            'hello_world_id': self.hello_world_id,
            'greeting': self.greeting,
        })
        return base_dict

    def __repr__(self) -> str:
        return f"HelloWorldUpdated(id={self.hello_world_id}, greeting={self.greeting})"
