from typing import Dict, List, Type
from Shared.Domain.Events.DomainEvent import DomainEvent
from Shared.Domain.Events.DomainEventSubscriber import DomainEventSubscriber
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface


class EventDispatcher(EventDispatcherInterface):
    """
    Despachador de eventos de dominio.
    
    Responsabilidades:
    - Registrar suscriptores para eventos específicos
    - Publicar eventos a todos los suscriptores registrados
    - Gestionar el ciclo de vida de los eventos
    
    Patrón: Observer/Publish-Subscribe
    """
    
    def __init__(self):
        # Diccionario: event_name -> List[DomainEventSubscriber]
        self._subscribers: Dict[str, List[DomainEventSubscriber]] = {}
    
    def subscribe(self, subscriber: DomainEventSubscriber) -> None:
        """
        Registra un suscriptor para uno o más tipos de evento.
        
        Soporta suscriptores que escuchan un solo evento o múltiples eventos.
        
        Args:
            subscriber: El suscriptor a registrar
        """
        subscribed_to = subscriber.subscribed_to()
        
        # Soportar tanto una clase única como una lista de clases
        event_classes = subscribed_to if isinstance(subscribed_to, list) else [subscribed_to]
        
        for event_class in event_classes:
            event_name = event_class.__name__
            
            if event_name not in self._subscribers:
                self._subscribers[event_name] = []
            
            # Evitar duplicados
            if subscriber not in self._subscribers[event_name]:
                self._subscribers[event_name].append(subscriber)
    
    def publish(self, event: DomainEvent) -> None:
        """
        Publica un evento a todos los suscriptores registrados.
        
        Args:
            event: El evento de dominio a publicar
        """
        event_name = event.event_name
        
        if event_name in self._subscribers:
            for subscriber in self._subscribers[event_name]:
                try:
                    subscriber.handle(event)
                except Exception as e:
                    # Log del error pero no interrumpir el flujo
                    print(f"Error al manejar evento {event_name} en {subscriber.__class__.__name__}: {str(e)}")
    
    def publish_multiple(self, events: List[DomainEvent]) -> None:
        """
        Publica múltiples eventos en orden.
        
        Args:
            events: Lista de eventos a publicar
        """
        for event in events:
            self.publish(event)
    
    def has_subscribers(self, event_class: Type[DomainEvent]) -> bool:
        """
        Verifica si hay suscriptores para un tipo de evento.
        
        Args:
            event_class: La clase del evento
            
        Returns:
            bool: True si hay suscriptores, False en caso contrario
        """
        event_name = event_class.__name__
        return event_name in self._subscribers and len(self._subscribers[event_name]) > 0
    
    def get_subscribers(self, event_class: Type[DomainEvent]) -> List[DomainEventSubscriber]:
        """
        Obtiene la lista de suscriptores para un tipo de evento.
        
        Args:
            event_class: La clase del evento
            
        Returns:
            List[DomainEventSubscriber]: Lista de suscriptores
        """
        event_name = event_class.__name__
        return self._subscribers.get(event_name, [])
    
    def clear_subscribers(self) -> None:
        """
        Elimina todos los suscriptores registrados.
        Útil para testing.
        """
        self._subscribers.clear()
