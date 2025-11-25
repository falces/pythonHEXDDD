from Shared.Application.CommandBus import CommandBus
from Application.Commands.CreateHelloWorldCommand import CreateHelloWorldCommand


class CreateHelloWorldUseCase:
    """
    Caso de Uso para crear una nueva entidad HelloWorld.
    Refactorizado para usar CommandBus (CQRS).
    Mantiene la interfaz original para compatibilidad.
    """

    def __init__(self, command_bus: CommandBus):
        self.command_bus = command_bus

    def execute(self, greeting_text: str) -> dict:
        """
        Ejecuta el caso de uso creando y despachando un comando.
        """
        # 1. Crear comando
        command = CreateHelloWorldCommand(greeting_text=greeting_text)

        # 2. Despachar al bus (retorna ID)
        entity_id = self.command_bus.dispatch(command)

        # 3. Retornar diccionario para mantener compatibilidad con controladores antiguos
        return {
            "id": entity_id,
            "greeting": greeting_text
        }
