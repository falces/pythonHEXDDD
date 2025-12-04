from Shared.Application.CommandHandler import CommandHandler
from Admin.Domain.Repository.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Admin.Application.Commands.DeleteUserCommand import DeleteUserCommand


class DeleteUserHandler(CommandHandler):
    """Handler para eliminar un usuario."""
    
    def __init__(
        self,
        write_repository: UserWriteRepositoryInterface,
        event_dispatcher: EventDispatcherInterface,
    ):
        self.write_repository = write_repository
        self.event_dispatcher = event_dispatcher
        
    def handle(self, command: DeleteUserCommand) -> bool:
        # Verificar que existe
        existing_user = self.write_repository.find_by_id(command.id)
        
        if existing_user is None:
            raise ValueError(f"User with id {command.id} not found")
        
        # Eliminar usuario
        self.write_repository.delete(command.id)
        
        # Aquí podrías registrar un evento UserDeleted si lo necesitas
        
        return True
