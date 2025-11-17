from Shared.Domain.Events.DomainEvent import DomainEvent
from Shared.Domain.Events.DomainEventSubscriber import DomainEventSubscriber
from Domain.HelloWorld.Events.HelloWorldCreated import HelloWorldCreated
from config.log import logger


class HelloWorldCreatedLogger(DomainEventSubscriber):
    """
    Handler que registra en el log cuando se crea un HelloWorld.
    
    Este handler demuestra cómo implementar logging de eventos
    de dominio para auditoría y debugging.
    """
    
    def subscribed_to(self):
        """Suscrito al evento HelloWorldCreated."""
        return HelloWorldCreated
    
    def handle(self, event: HelloWorldCreated) -> None:
        """
        Registra en el log la creación del HelloWorld.
        
        Args:
            event: El evento HelloWorldCreated
        """
        logger.info(
            f"[DOMAIN EVENT] HelloWorld creado - "
            f"ID: {event.hello_world_id}, "
            f"Greeting: '{event.greeting}', "
            f"Timestamp: {event.occurred_on}"
        )
