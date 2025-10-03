from flask import Blueprint, request
from Application.HelloWorldService import HelloWorldService
from Infrastructure.Repository.HelloWorldRepository import HelloWorldRepository
from Infrastructure.Controller.ControllerBase import ControllerBase


helloWorldController = Blueprint('helloWorldController', __name__)

class HelloWorldController():

    @helloWorldController.route('/', methods=['GET'])
    def getAllGreetings():
        helloWorldService = HelloWorldService(HelloWorldRepository)

        return ControllerBase.formatResponse(
            helloWorldService.getAllHelloWorld(),
            200,
        )