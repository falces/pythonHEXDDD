from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Domain.HelloWorld.Events.HelloWorldDeleted import HelloWorldDeleted
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher


class DeleteHelloWorldUseCase:
    """
    Caso de Uso: Eliminar un HelloWorld por su ID.
    
    Responsabilidades:
    - Validar que el ID sea válido
    - Eliminar la entidad del repositorio
    - Publicar eventos de dominio
    - Retornar el resultado de la operación
    """
    
    def __init__(self, repository: HelloWorldRepositoryInterface, event_dispatcher: EventDispatcher):
        self.repository = repository
        self.event_dispatcher = event_dispatcher
    
    def execute(self, hello_world_id: int) -> bool:
        """
        Ejecuta el caso de uso de eliminar un HelloWorld.
        
        Args:
            hello_world_id: ID del HelloWorld a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        # Primero verificar si existe (opcional, pero útil para el evento)
        entity = self.repository.findById(hello_world_id)
        
        if not entity:
            return False
        
        # Eliminar usando el repositorio
        deleted = self.repository.delete(hello_world_id)
        
        # Si se eliminó correctamente, publicar evento
        if deleted:
            event = HelloWorldDeleted(hello_world_id=hello_world_id)
            self.event_dispatcher.publish(event)
        
        return deleted
