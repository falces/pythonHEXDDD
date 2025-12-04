from Shared.Application.CommandHandler import CommandHandler
from Admin.Domain.Repository.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Admin.Domain.Repository.UserReadRepositoryInterface import UserReadRepositoryInterface
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Admin.Application.Commands.UpdateUserCommand import UpdateUserCommand
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject


class UpdateUserHandler(CommandHandler):
    """Handler para actualizar un usuario."""
    
    def __init__(
        self,
        write_repository: UserWriteRepositoryInterface,
        read_repository: UserReadRepositoryInterface,
        event_dispatcher: EventDispatcherInterface,
    ):
        self.write_repository = write_repository
        self.read_repository = read_repository
        self.event_dispatcher = event_dispatcher
        
    def handle(self, command: UpdateUserCommand) -> str:
        # Buscar usuario existente
        existing_user = self.write_repository.find_by_id(command.id)
        
        if existing_user is None:
            raise ValueError(f"User with id {command.id} not found")
        
        # Actualizar campos si se proporcionan
        if command.username:
            existing_user.username = UsernameValueObject.create(command.username)
        
        if command.email:
            existing_user.email = EmailValueObject.create(command.email)
        
        # Persistir cambios
        saved_user = self.write_repository.save(existing_user)
        
        # Publicar eventos si los hay
        events = saved_user.pull_domain_events()
        if events:
            self.event_dispatcher.publish_multiple(events)
        
        return saved_user.id.value
