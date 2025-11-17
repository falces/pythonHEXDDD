from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.Greeting import Greeting
from Infrastructure.Persistence.Mappers.HelloWorldMapper import HelloWorldMapper
from config.signals import signals
import uuid
from Application.DTO import GreetingDTO


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
        all_hello_world = self.repository.findAll()

        # Usar el mapper para convertir entidades a diccionarios
        hello_world_list = []
        for hello_world in all_hello_world:
            hello_world_list.append(HelloWorldMapper.toDict(hello_world))

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
        result_dict = HelloWorldMapper.toDict(saved_entity)
        signals['new_hello_world'].send(
            sender=uuid.uuid4().hex,
            message=result_dict,
        )
        
        return result_dict

