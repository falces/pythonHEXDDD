from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.Greeting import Greeting
from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Infrastructure.Persistence.Mappers.HelloWorldMapper import HelloWorldMapper
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher


class CreateHelloWorldUseCase:
    """
    Caso de Uso para crear una nueva entidad HelloWorld.
    Su única responsabilidad es orquestar la creación y persistencia.
    """

    def __init__(self, repository: HelloWorldRepositoryInterface, event_dispatcher: EventDispatcher):
        self.repository = repository
        self.event_dispatcher = event_dispatcher

    def execute(self, greeting_text: str) -> dict:
        # 1. Crear Value Object (contiene validaciones de dominio)
        greeting = Greeting.create(greeting_text)

        # 2. Crear la entidad de dominio y registrar eventos
        hello_world = HelloWorld.create(greeting=greeting)

        # 3. Persistir la entidad a través del repositorio
        saved_entity = self.repository.save(hello_world)

        # 4. Publicar los eventos de dominio registrados
        self.event_dispatcher.publish_multiple(saved_entity.pull_domain_events())

        # 5. Serializar la entidad a un diccionario para la respuesta
        return HelloWorldMapper.toDict(saved_entity)