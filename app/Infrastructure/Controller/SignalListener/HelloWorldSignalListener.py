from app import signals
from flask import Blueprint
from Infrastructure.Repository.HelloWorldRepository import HelloWorldRepository
from Application.HelloWorldService import HelloWorldService
from Application.DTO.GreetingDTO import GreetingDTO

helloWorldSignalListener = Blueprint('helloWorldSignalListener', __name__)

class HelloWorldSignalListener():

    @signals['new_hello_world'].connect
    def newCountryListener(
        self,
        sender: str,
        message: dict,
    ):
        countryDTO = GreetingDTO(
            name = message['name'],
        )

        statusService = HelloWorldService(HelloWorldRepository)
        statusService.addCountry(countryDTO)