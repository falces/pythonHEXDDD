from abc import ABC, abstractmethod
from typing import List
from Shared.Domain.Events.DomainEvent import DomainEvent


class EventDispatcherInterface(ABC):
    """
    Interfaz para el Event Dispatcher.
    
    Define el contrato que debe cumplir cualquier implementación
    de dispatcher de eventos de dominio.
    Esta interfaz pertenece al dominio (Dependency Inversion Principle).
    """
    
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """
        Publica un único evento de dominio.
        
        Args:
            event: Evento de dominio a publicar
        """
        pass
    
    @abstractmethod
    def publish_multiple(self, events: List[DomainEvent]) -> None:
        """
        Publica múltiples eventos de dominio.
        
        Args:
            events: Lista de eventos de dominio a publicar
        """
        pass
