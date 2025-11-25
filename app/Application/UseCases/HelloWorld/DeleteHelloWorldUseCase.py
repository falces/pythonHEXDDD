from Shared.Application.CommandBus import CommandBus
from Application.Commands.DeleteHelloWorldCommand import DeleteHelloWorldCommand


class DeleteHelloWorldUseCase:
    """
    Caso de Uso: Eliminar un HelloWorld por su ID.
    Refactorizado para usar CommandBus (CQRS).
    """

    def __init__(self, command_bus: CommandBus):
        self.command_bus = command_bus

    def execute(self, hello_world_id: int) -> bool:
        """
        Ejecuta el caso de uso despachando un comando de eliminación.

        Args:
            hello_world_id: ID del HelloWorld a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        command = DeleteHelloWorldCommand(id=hello_world_id)
        return self.command_bus.dispatch(command)
