from config.signals import signals
from flask import Blueprint
from Infrastructure.Repository.HelloWorldWriteRepository import HelloWorldWriteRepository
from Application.HelloWorldService import HelloWorldService
from Application.DTO.GreetingDTO import GreetingDTO

hello_world_signal_listener = Blueprint('helloWorldSignalListener', __name__)

class HelloWorldSignalListener():

    @signals['new_hello_world'].connect
    def new_country_listener(
        self,
        sender: str,
        message: dict,
    ):
        """
        Listener para el evento de nuevo HelloWorld.
        Nota: Este patrón debería moverse a usar eventos de dominio propiamente.
        """
        countryDTO = GreetingDTO(
            name = message['greeting'],
        )

        # Instanciar el repositorio y pasarlo al servicio
        repository = HelloWorldWriteRepository()
        statusService = HelloWorldService(repository)
        statusService.addHelloWorld(countryDTO)