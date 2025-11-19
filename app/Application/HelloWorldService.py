from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.Greeting import Greeting
from Application.Serializers.HelloWorldSerializer import HelloWorldSerializer
from config.signals import signals
import uuid
from Application.DTO.GreetingDTO import GreetingDTO


class HelloWorldService:
    """
    Servicio de aplicación para HelloWorld.
    Orquesta las operaciones de dominio y coordina con repositorios.
    """
    
    def __init__(
        self,
        repository: HelloWorldRepositoryInterface,
    ):
        # Recibe la instancia del repositorio (Inyección de Dependencias)
        self.repository = repository

    def getAllHelloWorld(
        self,
    ) -> list:
        """
        Obtiene todos los HelloWorld y los serializa a diccionarios.
        """
        all_hello_world = self.repository.find_all()

        # Usar el serializer para convertir entidades a diccionarios
        hello_world_list = []
        for hello_world in all_hello_world:
            hello_world_list.append(HelloWorldSerializer.to_dict(hello_world))

        return hello_world_list
    
    def addHelloWorld(
        self,
        greetingDTO: GreetingDTO,
    ) -> dict:
        """
        Crea un nuevo HelloWorld.
        """
        # Crear value object
        greeting = Greeting.create(greetingDTO.name)
        
        # Crear entidad de dominio
        hello_world = HelloWorld(greeting=greeting)

        # Persistir usando el repositorio
        saved_entity = self.repository.save(hello_world)

        # Emitir señal con el resultado
        result_dict = HelloWorldSerializer.to_dict(saved_entity)
        signals['new_hello_world'].send(
            sender=uuid.uuid4().hex,
            message=result_dict,
        )
        
        return result_dict

