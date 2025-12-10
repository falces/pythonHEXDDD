from Shared.Application.CommandHandler import CommandHandler
from Admin.Domain.Repository.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Admin.Application.Commands.CreateUserCommand import CreateUserCommand
from Admin.Domain.User import User
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject


class CreateUserHander(CommandHandler):
    
    def __init__(
        self,
        write_repository: UserWriteRepositoryInterface,
        event_dispatcher: EventDispatcherInterface,
    ):
        self.write_repository = write_repository
        self.event_dispatcher = event_dispatcher
        
    def handle(
        self,
        command: CreateUserCommand,
    ) -> str:
        username = UsernameValueObject.create(command.username)
        email = EmailValueObject.create(command.email)
        user = User.create(
            username=username,
            email=email,
        )
        self.write_repository.save(user)
        return user.id.value