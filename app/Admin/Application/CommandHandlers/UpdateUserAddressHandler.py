from Shared.Application.CommandHandler import CommandHandler
from Admin.Domain.Repository.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Admin.Application.Commands.UpdateUserAddressCommand import UpdateUserAddressCommand
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class UpdateUserAddressHandler(CommandHandler):
    """Handler para actualizar una dirección de un usuario."""
    
    def __init__(
        self,
        write_repository: UserWriteRepositoryInterface,
        event_dispatcher: EventDispatcherInterface,
    ):
        self.write_repository = write_repository
        self.event_dispatcher = event_dispatcher
        
    def handle(self, command: UpdateUserAddressCommand) -> str:
        """
        Actualiza una dirección existente del usuario.
        
        Args:
            command: Comando con los datos a actualizar
            
        Returns:
            str: ID de la dirección actualizada
            
        Raises:
            ValueError: Si el usuario o la dirección no existe
        """
        # Buscar usuario existente
        user = self.write_repository.find_by_id(command.user_id)
        
        if user is None:
            raise ValueError(f"User with id {command.user_id} not found")
        
        # Buscar la dirección
        address_id = UuidValueObject.create(command.address_id)
        address = user.get_address(address_id)
        
        if address is None:
            raise ValueError(f"Address with id {command.address_id} not found")
        
        # Actualizar los campos de la dirección
        address.update(
            street=command.street,
            city=command.city,
            country=command.country,
        )
        
        # Persistir cambios
        saved_user = self.write_repository.save(user)
        
        # Publicar eventos si los hay
        events = saved_user.pull_domain_events()
        if events:
            self.event_dispatcher.publish_multiple(events)
        
        return address.id.value
