from flask import Blueprint
from Admin.Infrastructure.Controller.AdminUserController import admin_user_controller


v1_controller_base = Blueprint('v1', __name__)

v1_controller_base.register_blueprint(admin_user_controller, url_prefix='/admin/user')
