from Shared.Application.CommandHandler import CommandHandler
from Admin.Domain.Repository.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Admin.Application.Commands.AddUserAddressCommand import AddUserAddressCommand


class AddUserAddressHandler(CommandHandler):
    """Handler para añadir una dirección a un usuario."""
    
    def __init__(
        self,
        write_repository: UserWriteRepositoryInterface,
        event_dispatcher: EventDispatcherInterface,
    ):
        self.write_repository = write_repository
        self.event_dispatcher = event_dispatcher
        
    def handle(self, command: AddUserAddressCommand) -> str:
        """
        Añade una nueva dirección al usuario.
        
        Args:
            command: Comando con los datos de la dirección
            
        Returns:
            str: ID de la dirección creada
            
        Raises:
            ValueError: Si el usuario no existe
        """
        # Buscar usuario existente
        user = self.write_repository.find_by_id(command.user_id)
        
        if user is None:
            raise ValueError(f"User with id {command.user_id} not found")
        
        # Añadir dirección al agregado (esto registra el evento internamente)
        address = user.add_address(
            street=command.street,
            city=command.city,
            country=command.country,
        )
        
        # Persistir cambios
        saved_user = self.write_repository.save(user)
        
        # Publicar eventos
        events = saved_user.pull_domain_events()
        if events:
            self.event_dispatcher.publish_multiple(events)
        
        return address.id.value
