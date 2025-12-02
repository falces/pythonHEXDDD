"""
Handler para procesar el comando DeleteHelloWorldCommand.
"""

from Application.Commands.DeleteHelloWorldCommand import DeleteHelloWorldCommand
from Domain.HelloWorld.HelloWorldWriteRepositoryInterface import HelloWorldWriteRepositoryInterface
from Domain.HelloWorld.HelloWorldReadRepositoryInterface import HelloWorldReadRepositoryInterface
from Domain.HelloWorld.Events.HelloWorldDeleted import HelloWorldDeleted
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Shared.Application.CommandHandler import CommandHandler


class DeleteHelloWorldHandler(CommandHandler):
    """
    Maneja la eliminación de HelloWorld.
    En CQRS puro: usa read_repository para validación y write_repository para eliminar.
    """

    def __init__(
        self,
        write_repository: HelloWorldWriteRepositoryInterface,
        read_repository: HelloWorldReadRepositoryInterface,
        event_dispatcher: EventDispatcherInterface
    ):
        self.write_repository = write_repository
        self.read_repository = read_repository
        self.event_dispatcher = event_dispatcher

    def handle(self, command: DeleteHelloWorldCommand) -> bool:
        """
        Procesa el comando de eliminación.

        Args:
            command: Comando con el ID a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        # 1. Verificar que existe usando read repository (CQRS puro)
        hello_world = self.read_repository.find_by_id(command.id)

        if hello_world is None:
            return False

        # 2. Eliminar del repositorio
        deleted = self.write_repository.delete(command.id)

        # 3. Publicar evento de eliminación si fue exitoso
        if deleted:
            event = HelloWorldDeleted(
                hello_world_id=command.id
            )
            self.event_dispatcher.publish(event)

        return deleted
