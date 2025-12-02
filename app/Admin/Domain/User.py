from typing import Self
import uuid
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Shared.Domain.Entities.EntityBase import AggregateRootBase
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject
from Admin.Domain.Events.UserCreated import UserCreated


class User(AggregateRootBase):
    
    def __init__(
        self,
        username: UsernameValueObject,
        email: EmailValueObject,
        id: UuidValueObject = None,
    ):
        super().__init__()
        
        if id is None:
            id = UuidValueObject.create(str(uuid.uuid4()))
        
        self.id = id
        self.username = username
        self.email = email
        
    @staticmethod
    def create(
        username: UsernameValueObject,
        email: EmailValueObject,
        id: UuidValueObject = None,
    ) -> Self:
        return User(
            username=username,
            email=email,
            id=id,
        )
        
    def mark_as_created(self) -> None:
        event = UserCreated(
            user_id=self.id.value,
            username=self.username.value,
            email=self.email.value,
        )
        self.record_event(event)
