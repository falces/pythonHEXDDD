from Shared.Application.CommandHandler import CommandHandler
from Admin.Domain.Repository.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Admin.Application.Commands.RemoveUserAddressCommand import RemoveUserAddressCommand
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class RemoveUserAddressHandler(CommandHandler):
    """Handler para eliminar una dirección de un usuario."""
    
    def __init__(
        self,
        write_repository: UserWriteRepositoryInterface,
        event_dispatcher: EventDispatcherInterface,
    ):
        self.write_repository = write_repository
        self.event_dispatcher = event_dispatcher
        
    def handle(self, command: RemoveUserAddressCommand) -> bool:
        """
        Elimina una dirección del usuario.
        
        Args:
            command: Comando con los IDs del usuario y la dirección
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            ValueError: Si el usuario o la dirección no existe
        """
        # Buscar usuario existente
        user = self.write_repository.find_by_id(command.user_id)
        
        if user is None:
            raise ValueError(f"User with id {command.user_id} not found")
        
        # Eliminar la dirección del agregado (esto registra el evento internamente)
        address_id = UuidValueObject.create(command.address_id)
        removed = user.remove_address(address_id)
        
        if not removed:
            raise ValueError(f"Address with id {command.address_id} not found")
        
        # Persistir cambios (transacción y eventos centralizados en el repositorio)
        self.write_repository.save(user)
        return True
