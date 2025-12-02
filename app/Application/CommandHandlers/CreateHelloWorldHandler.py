"""
Handler para procesar el comando CreateHelloWorldCommand.
"""

from Application.Commands.CreateHelloWorldCommand import CreateHelloWorldCommand
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
from Domain.HelloWorld.HelloWorldWriteRepositoryInterface import HelloWorldWriteRepositoryInterface
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Shared.Application.CommandHandler import CommandHandler


class CreateHelloWorldHandler(CommandHandler):
    """
    Maneja la creación de HelloWorld.
    Encapsula la lógica de negocio para crear entidades.
    """

    def __init__(
        self,
        write_repository: HelloWorldWriteRepositoryInterface,
        event_dispatcher: EventDispatcherInterface
    ):
        self.write_repository = write_repository
        self.event_dispatcher = event_dispatcher

    def handle(self, command: CreateHelloWorldCommand) -> int:
        """
        Procesa el comando de creación.

        Args:
            command: Comando con los datos para crear

        Returns:
            int: ID de la entidad creada

        Raises:
            IncorrectGreetingException: Si el greeting es inválido
        """
        # 1. Crear Value Object (con validaciones de dominio)
        greeting = GreetingValueObject.create(command.greeting_text)

        # 2. Crear entidad de dominio (registra eventos)
        hello_world = HelloWorld.create(greeting=greeting)

        # 3. Persistir a través del repositorio
        saved_entity = self.write_repository.save(hello_world)

        # 4. Marcar como creado para registrar el evento (ahora que tenemos el ID)
        saved_entity.mark_as_created(saved_entity.id)

        # 5. Publicar eventos de dominio
        self.event_dispatcher.publish_multiple(
            saved_entity.pull_domain_events())

        # 5. Retornar solo el ID (sin exponer el modelo de dominio)
        return saved_entity.id
