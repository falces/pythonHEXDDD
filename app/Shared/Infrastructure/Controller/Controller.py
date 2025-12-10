from flask import Blueprint
from Infrastructure.Controller.MoviesController import movies_controller
# from Infrastructure.Controller.SignalListener.HelloWorldSignalListener import hello_world_signal_listener
from Infrastructure.Controller.HelloWorldController import hello_world_controller
from Admin.Infrastructure.Controller.AdminUserController import admin_user_controller


v1_controller_base = Blueprint('v1', __name__)

v1_controller_base.register_blueprint(movies_controller, url_prefix='/movies')
# v1_controller_base.register_blueprint(hello_world_controller, url_prefix='/hello-world')
# v1_controller_base.register_blueprint(hello_world_signal_listener)
v1_controller_base.register_blueprint(admin_user_controller, url_prefix='/admin/user')
