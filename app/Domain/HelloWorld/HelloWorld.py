from Domain.HelloWorld.ValueObjects.Greeting import Greeting
from Shared.Domain.Entities.EntityBase import AggregateRootBase
from Domain.HelloWorld.HelloWorldModel import HelloWorldModel

class HelloWorld(AggregateRootBase):
    def __init__(
        self,
        greeting: Greeting,
    ):
        self.name = greeting

        self.model = HelloWorldModel(
            greeting=self.name.getValue(),
        )

    def toDict(self) -> dict:
        return self.model.toDict()