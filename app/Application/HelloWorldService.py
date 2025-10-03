from Shared.Domain.Repositories.AbstractRepository import AbstractRepository
from Domain.HelloWorld import HelloWorld
from app import app, signals
import uuid
from Application.DTO import GreetingDTO

class HelloWorldService:
    def __init__(
        self,
        repository: AbstractRepository,
    ):
        self.repository = repository()

    def getAllHelloWorld(
        self,
    ) -> list:
        allHelloWord = self.repository.findAll()

        helloWorldGreetings = []
        for helloWorld in allHelloWord:
            helloWorldGreetings.append(helloWorld.toDict())

        return helloWorldGreetings
    
    def addCountry(
        self,
        greetingDTO: GreetingDTO,
    ):
        greeting = HelloWorld(
            name = greetingDTO.name,
        )

        self.repository.save(greeting)

        signals['new_hello_world'].send(
            sender=uuid.uuid4().hex,
            message=greeting.toDict(),
        )

