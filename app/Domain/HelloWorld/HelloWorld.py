from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
from Domain.HelloWorld.Events.HelloWorldCreated import HelloWorldCreated
from Shared.Domain.Entities.EntityBase import AggregateRootBase


class HelloWorld(AggregateRootBase):
    """
    Entidad de dominio HelloWorld - Aggregate Root.
    Esta entidad es pura y no conoce detalles de persistencia.
    """

    def __init__(
        self,
        greeting: GreetingValueObject,
        id: int = None
    ):
        super().__init__()
        self._id = id
        self.greeting = greeting

    @staticmethod
    def create(greeting: GreetingValueObject) -> 'HelloWorld':
        """
        Factory method para crear un nuevo HelloWorld.
        Registra automáticamente el evento de creación.

        Args:
            greeting: El saludo a crear

        Returns:
            HelloWorld: Nueva instancia con evento registrado
        """
        hello_world = HelloWorld(greeting=greeting)
        # El evento se registrará después de tener el ID (en el use case)
        return hello_world

    def mark_as_created(self, id: int) -> None:
        """
        Marca el HelloWorld como creado y registra el evento.
        Se llama después de persistir en el repositorio cuando ya tenemos el ID.

        Args:
            id: El ID asignado por la base de datos
        """
        self._id = id
        event = HelloWorldCreated(
            hello_world_id=id,
            greeting=self.greeting.value
        )
        self.record_event(event)

    @property
    def id(self) -> int:
        """ID del HelloWorld."""
        return self._id
