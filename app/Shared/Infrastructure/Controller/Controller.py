from flask import Blueprint
from Infrastructure.Controller.MoviesController import moviesController
# from Infrastructure.Controller.SignalListener.HelloWorldSignalListener import helloWorldSignalListener


v1ControllerBase = Blueprint('v1', __name__)

v1ControllerBase.register_blueprint(moviesController, url_prefix='/movies')
# v1ControllerBase.register_blueprint(helloWorldSignalListener)