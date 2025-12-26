from Shared.Application.CommandHandler import CommandHandler
from Admin.Domain.Repository.UserWriteRepositoryInterface import UserWriteRepositoryInterface
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Admin.Application.Commands.CreateUserCommand import CreateUserCommand
from Admin.Domain.User import User


class CreateUserHandler(CommandHandler):

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
        user = User.create(
            username=command.username,
            email=command.email,
        )
        user.mark_as_created()

        self.write_repository.save(user)
        self.event_dispatcher.publish_multiple(user.pull_domain_events())

        return user.id.value
