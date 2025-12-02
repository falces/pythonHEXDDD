import traceback
from flask import Blueprint, request, current_app
from Shared.Infrastructure.Controller.ControllerBase import ControllerBase
from Admin.Application.Commands.CreateUserCommand import CreateUserCommand
from Admin.Application.Queries.GetUserByIdQuery import GetUserByIdQuery
from Admin.Infrastructure.Validators.RequestValidators import CreateUserValidator


admin_user_controller = Blueprint('adminUserController', __name__)


class AdminUserController:
    
    @admin_user_controller.route('/', methods=['POST'])
    def create_user():
        try:
            data = request.get_json()
            
            validator = CreateUserValidator(data)
            if not validator.is_valid():
                return ControllerBase.format_response(
                    {"errors": validator.get_errors()},
                    400
                )
            
            create_user_command = CreateUserCommand(
                username=data['username'],
                email=data['email'],
            )
            
            create_user_command_bus = current_app.container.command_bus()
            user_id = create_user_command_bus.dispatch(create_user_command)
            
            query = GetUserByIdQuery(id=user_id)
            
            query_bus = current_app.container.query_bus()
            created_user = query_bus.dispatch(query)
            
            return ControllerBase.format_response(
                created_user,
                201
            )

        except Exception as e:
            return ControllerBase.format_response(
                {
                    "error": str(e),
                    "traceback": traceback.format_exc()
                },
                e.code if hasattr(e, 'code') else 500
            )