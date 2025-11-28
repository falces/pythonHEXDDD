from Shared.Domain.Events.DomainEventSubscriber import DomainEventSubscriber
from Domain.HelloWorld.Events.HelloWorldUpdated import HelloWorldUpdated
from config.log import logger


class HelloWorldUpdatedLogger(DomainEventSubscriber):
    """
    Handler que registra en el log cuando se actualiza un HelloWorld.

    Este handler demuestra cómo implementar logging de eventos
    de dominio para auditoría y debugging.
    """

    def subscribed_to(self):
        """Suscrito al evento HelloWorldUpdated."""
        return HelloWorldUpdated

    def handle(self, event: HelloWorldUpdated) -> None:
        """
        Registra en el log la actualización del HelloWorld.

        Args:
            event: El evento HelloWorldCreated
        """
        logger.info(
            f"[DOMAIN EVENT] HelloWorld actualizado - "
            f"ID: {event.hello_world_id}, "
            f"Greeting: '{event.greeting}', "
            f"Timestamp: {event.occurred_on}"
        )
