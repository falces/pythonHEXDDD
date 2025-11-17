from abc import ABC, abstractmethod
from typing import Type
from Shared.Domain.Events.DomainEvent import DomainEvent


class DomainEventSubscriber(ABC):
    """
    Interfaz para los suscriptores de eventos de dominio.
    
    Los handlers que quieran reaccionar a eventos de dominio
    deben implementar esta interfaz.
    """
    
    @abstractmethod
    def subscribed_to(self) -> Type[DomainEvent]:
        """
        Retorna la clase del evento al que está suscrito este handler.
        
        Returns:
            Type[DomainEvent]: Clase del evento
        """
        pass
    
    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        """
        Maneja el evento de dominio.
        
        Args:
            event: El evento de dominio a manejar
        """
        pass
