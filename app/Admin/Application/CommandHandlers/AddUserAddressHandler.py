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
        Añade una nueva dirección al usuario (Deferred Pattern: sin commit ni publicación de eventos aquí).
        """
        # Buscar usuario existente
        user = self.write_repository.find_by_id(command.user_id)
        if user is None:
            raise ValueError(f"User with id {command.user_id} not found")
        # Modificar el agregado (esto registra el evento internamente)
        address = user.add_address(
            street=command.street,
            city=command.city,
            country=command.country,
        )
        # Persistir cambios (transacción y eventos centralizados en el repositorio)
        self.write_repository.save(user)
        return address.id.value
