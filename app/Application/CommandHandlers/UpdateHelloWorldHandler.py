"""
Handler para procesar el comando UpdateHelloWorldCommand.
"""

from Application.Commands.UpdateHelloWorldCommand import UpdateHelloWorldCommand
from Domain.HelloWorld.ValueObjects.Greeting import Greeting
from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Infrastructure.Repository.HelloWorldReadRepository import HelloWorldReadRepository
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher


class UpdateHelloWorldHandler:
    """
    Maneja la actualización de HelloWorld.
    En CQRS puro: usa read_repository para validación y write_repository para persistir.
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
    
    def handle(self, command: UpdateHelloWorldCommand) -> bool:
        """
        Procesa el comando de actualización.
        
        Args:
            command: Comando con los datos para actualizar
            
        Returns:
            bool: True si se actualizó correctamente
            
        Raises:
            ValueError: Si la entidad no existe
            IncorrectGreetingException: Si el greeting es inválido
        """
        # 1. Buscar entidad existente usando read repository (CQRS puro)
        hello_world = self.read_repository.findById(command.id)
        
        if hello_world is None:
            raise ValueError(f"HelloWorld with id {command.id} not found")
        
        # 2. Crear nuevo Value Object con validaciones
        new_greeting = Greeting.create(command.greeting_text)
        
        # 3. Actualizar la entidad
        hello_world.greeting = new_greeting
        
        # 4. Persistir cambios
        self.repository.save(hello_world)
        
        # 5. Publicar eventos si los hay
        events = hello_world.pull_domain_events()
        if events:
            self.event_dispatcher.publish_multiple(events)
        
        return True
