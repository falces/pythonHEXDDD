from flask import Blueprint
from Infrastructure.Controller.HelloWorldController import helloWorldController
from Infrastructure.Controller.SignalListener.HelloWorldSignalListener import helloWorldSignalListener


v1ControllerBase = Blueprint('v1', __name__)

v1ControllerBase.register_blueprint(helloWorldController, url_prefix='/helloWorld')
v1ControllerBase.register_blueprint(helloWorldSignalListener)