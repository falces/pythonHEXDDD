"""
Handler para procesar el comando DeleteHelloWorldCommand.
"""

from Application.Commands.DeleteHelloWorldCommand import DeleteHelloWorldCommand
from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Infrastructure.Repository.HelloWorldReadRepository import HelloWorldReadRepository
from Domain.HelloWorld.Events.HelloWorldDeleted import HelloWorldDeleted
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher


class DeleteHelloWorldHandler:
    """
    Maneja la eliminación de HelloWorld.
    En CQRS puro: usa read_repository para validación y write_repository para eliminar.
    """
    
    def __init__(
        self,
        repository: HelloWorldRepositoryInterface,
        read_repository: HelloWorldReadRepository,
        event_dispatcher: EventDispatcher
    ):
        self.repository = repository
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
        hello_world = self.read_repository.findById(command.id)
        
        if hello_world is None:
            return False
        
        # 2. Eliminar del repositorio
        deleted = self.repository.delete(command.id)
        
        # 3. Publicar evento de eliminación si fue exitoso
        if deleted:
            event = HelloWorldDeleted(
                hello_world_id=command.id
            )
            self.event_dispatcher.publish(event)
        
        return deleted
