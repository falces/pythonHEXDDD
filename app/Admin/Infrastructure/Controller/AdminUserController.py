import traceback
from flask import Blueprint, request, current_app
from Admin.Infrastructure.Persistence.Mappers.UserMapper import UserMapper
from Shared.Infrastructure.Controller.ControllerBase import ControllerBase
from Admin.Application.Commands.CreateUserCommand import CreateUserCommand
from Admin.Application.Queries.GetUserByIdQuery import GetUserByIdQuery


admin_user_controller = Blueprint('adminUserController', __name__)


class AdminUserController:
    
    @admin_user_controller.route('/', methods=['POST'])
    def create_user():
        try:
            data = request.get_json()
            
            # Comprobar body
            # if not data or 'greeting' not in data:
            #     return ControllerBase.format_response(
            #         {"error": "Field 'greeting' is required"},
            #         400
            #     )
            
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
            
            
        # except IncorrectGreetingException as e:
        #     return ControllerBase.format_response({"error": str(e)}, 400)

        except Exception as e:
            return ControllerBase.format_response(
                {
                    "error": str(e),
                    "traceback": traceback.format_exc()
                },
                e.code if hasattr(e, 'code') else 500
            )