from Shared.Domain.Events.DomainEvent import DomainEvent
from Shared.Domain.Events.DomainEventSubscriber import DomainEventSubscriber
from Domain.HelloWorld.Events.HelloWorldDeleted import HelloWorldDeleted
from config.log import logger


class HelloWorldDeletedLogger(DomainEventSubscriber):
    """
    Handler que registra en el log cuando se elimina un HelloWorld.
    
    Este handler demuestra cómo implementar logging de eventos
    de dominio para auditoría y debugging.
    """
    
    def subscribed_to(self):
        """Suscrito al evento HelloWorldDeleted."""
        return HelloWorldDeleted
    
    def handle(self, event: HelloWorldDeleted) -> None:
        """
        Registra en el log la eliminación del HelloWorld.
        
        Args:
            event: El evento HelloWorldDeleted
        """
        logger.info(
            f"[DOMAIN EVENT] HelloWorld eliminado - "
            f"ID: {event.hello_world_id}, "
            f"Timestamp: {event.occurred_on}"
        )
