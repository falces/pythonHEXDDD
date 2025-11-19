from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface
from Application.Serializers.HelloWorldSerializer import HelloWorldSerializer


class CreateHelloWorldUseCase:
    """
    Caso de Uso para crear una nueva entidad HelloWorld.
    Su única responsabilidad es orquestar la creación y persistencia.
    """

    def __init__(
            self,
            repository: HelloWorldRepositoryInterface,
            event_dispatcher: EventDispatcherInterface):
        self.repository = repository
        self.event_dispatcher = event_dispatcher

    def execute(self, greeting_text: str) -> dict:
        # 1. Crear Value Object (contiene validaciones de dominio)
        greeting = GreetingValueObject.create(greeting_text)

        # 2. Crear la entidad de dominio y registrar eventos
        hello_world = HelloWorld.create(greeting=greeting)

        # 3. Persistir la entidad a través del repositorio
        saved_entity = self.repository.save(hello_world)

        # 4. Marcar como creado para registrar el evento (ahora que tenemos el ID)
        saved_entity.mark_as_created(saved_entity.id)

        # 5. Publicar los eventos de dominio registrados
        self.event_dispatcher.publish_multiple(
            saved_entity.pull_domain_events())

        # 6. Serializar la entidad a un diccionario para la respuesta
        return HelloWorldSerializer.to_dict(saved_entity)
