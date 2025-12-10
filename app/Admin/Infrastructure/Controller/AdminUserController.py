import traceback
from flask import Blueprint, request, current_app
from Shared.Infrastructure.Controller.ControllerBase import ControllerBase
from Admin.Application.Commands.CreateUserCommand import CreateUserCommand
from Admin.Application.Commands.UpdateUserCommand import UpdateUserCommand
from Admin.Application.Commands.DeleteUserCommand import DeleteUserCommand
from Admin.Application.Commands.AddUserAddressCommand import AddUserAddressCommand
from Admin.Application.Commands.UpdateUserAddressCommand import UpdateUserAddressCommand
from Admin.Application.Commands.RemoveUserAddressCommand import RemoveUserAddressCommand
from Admin.Application.Queries.GetUserByIdQuery import GetUserByIdQuery
from Admin.Application.Queries.GetAllUsersQuery import GetAllUsersQuery
from Admin.Infrastructure.Validators.RequestValidators import (
    CreateUserValidator,
    UpdateUserValidator,
    AddUserAddressValidator,
    UpdateUserAddressValidator,
)


admin_user_controller = Blueprint('adminUserController', __name__)


class AdminUserController:
    
    @admin_user_controller.route('/', methods=['GET'])
    def get_all_users():
        """Obtiene todos los usuarios."""
        try:
            query = GetAllUsersQuery()
            query_bus = current_app.container.query_bus()
            users = query_bus.dispatch(query)
            
            return ControllerBase.format_response(users, 200)

        except Exception as e:
            return AdminUserController._handle_error(e)
    
    @admin_user_controller.route('/<user_id>', methods=['GET'])
    def get_user(user_id: str):
        """Obtiene un usuario por ID."""
        try:
            query = GetUserByIdQuery(id=user_id)
            query_bus = current_app.container.query_bus()
            user = query_bus.dispatch(query)
            
            if user is None:
                return ControllerBase.format_response(
                    {"error": "User not found"},
                    404
                )
            
            return ControllerBase.format_response(user, 200)

        except Exception as e:
            return AdminUserController._handle_error(e)
    
    @admin_user_controller.route('/', methods=['POST'])
    def create_user():
        """Crea un nuevo usuario."""
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
            
            command_bus = current_app.container.command_bus()
            user_id = command_bus.dispatch(create_user_command)
            
            query = GetUserByIdQuery(id=user_id)
            query_bus = current_app.container.query_bus()
            created_user = query_bus.dispatch(query)
            
            return ControllerBase.format_response(created_user, 201)

        except Exception as e:
            return AdminUserController._handle_error(e)
    
    @admin_user_controller.route('/<user_id>', methods=['PUT', 'PATCH'])
    def update_user(user_id: str):
        """Actualiza un usuario existente."""
        try:
            data = request.get_json()
            
            validator = UpdateUserValidator(data)
            if not validator.is_valid():
                return ControllerBase.format_response(
                    {"errors": validator.get_errors()},
                    400
                )
            
            update_command = UpdateUserCommand(
                id=user_id,
                username=data.get('username'),
                email=data.get('email'),
            )
            
            command_bus = current_app.container.command_bus()
            command_bus.dispatch(update_command)
            
            # Devolver usuario actualizado
            query = GetUserByIdQuery(id=user_id)
            query_bus = current_app.container.query_bus()
            updated_user = query_bus.dispatch(query)
            
            return ControllerBase.format_response(updated_user, 200)

        except ValueError as e:
            if "not found" in str(e):
                return ControllerBase.format_response(
                    {"error": str(e)},
                    404
                )
            return AdminUserController._handle_error(e)
        except Exception as e:
            return AdminUserController._handle_error(e)
    
    @admin_user_controller.route('/<user_id>', methods=['DELETE'])
    def delete_user(user_id: str):
        """Elimina un usuario."""
        try:
            delete_command = DeleteUserCommand(id=user_id)
            
            command_bus = current_app.container.command_bus()
            command_bus.dispatch(delete_command)
            
            return '', 204

        except ValueError as e:
            if "not found" in str(e):
                return ControllerBase.format_response(
                    {"error": str(e)},
                    404
                )
            return AdminUserController._handle_error(e)
        except Exception as e:
            return AdminUserController._handle_error(e)
    
    # ========== ENDPOINTS DE DIRECCIONES (UserAddress) ==========
    
    @admin_user_controller.route('/<user_id>/addresses', methods=['GET'])
    def get_user_addresses(user_id: str):
        """Obtiene todas las direcciones de un usuario."""
        try:
            query = GetUserByIdQuery(id=user_id)
            query_bus = current_app.container.query_bus()
            user = query_bus.dispatch(query)
            
            if user is None:
                return ControllerBase.format_response(
                    {"error": "User not found"},
                    404
                )
            
            addresses = user.get("addresses", [])
            return ControllerBase.format_response(addresses, 200)

        except Exception as e:
            return AdminUserController._handle_error(e)
    
    @admin_user_controller.route('/<user_id>/addresses/<address_id>', methods=['GET'])
    def get_user_address(user_id: str, address_id: str):
        """Obtiene una dirección específica de un usuario."""
        try:
            query = GetUserByIdQuery(id=user_id)
            query_bus = current_app.container.query_bus()
            user = query_bus.dispatch(query)
            
            if user is None:
                return ControllerBase.format_response(
                    {"error": "User not found"},
                    404
                )
            
            addresses = user.get("addresses", [])
            address = next(
                (addr for addr in addresses if addr.get("id") == address_id),
                None
            )
            
            if address is None:
                return ControllerBase.format_response(
                    {"error": "Address not found"},
                    404
                )
            
            return ControllerBase.format_response(address, 200)

        except Exception as e:
            return AdminUserController._handle_error(e)
    
    @admin_user_controller.route('/<user_id>/addresses', methods=['POST'])
    def add_user_address(user_id: str):
        """Añade una nueva dirección a un usuario."""
        try:
            data = request.get_json()
            
            validator = AddUserAddressValidator(data)
            if not validator.is_valid():
                return ControllerBase.format_response(
                    {"errors": validator.get_errors()},
                    400
                )
            
            add_address_command = AddUserAddressCommand(
                user_id=user_id,
                street=data['street'],
                city=data['city'],
                country=data['country'],
            )
            
            command_bus = current_app.container.command_bus()
            address_id = command_bus.dispatch(add_address_command)
            
            # Devolver el usuario actualizado con la nueva dirección
            query = GetUserByIdQuery(id=user_id)
            query_bus = current_app.container.query_bus()
            user = query_bus.dispatch(query)
            
            # Buscar la dirección recién creada
            addresses = user.get("addresses", [])
            new_address = next(
                (addr for addr in addresses if addr.get("id") == address_id),
                None
            )
            
            return ControllerBase.format_response(new_address, 201)

        except ValueError as e:
            if "not found" in str(e):
                return ControllerBase.format_response(
                    {"error": str(e)},
                    404
                )
            return AdminUserController._handle_error(e)
        except Exception as e:
            return AdminUserController._handle_error(e)
    
    @admin_user_controller.route('/<user_id>/addresses/<address_id>', methods=['PUT', 'PATCH'])
    def update_user_address(user_id: str, address_id: str):
        """Actualiza una dirección de un usuario."""
        try:
            data = request.get_json()
            
            validator = UpdateUserAddressValidator(data)
            if not validator.is_valid():
                return ControllerBase.format_response(
                    {"errors": validator.get_errors()},
                    400
                )
            
            update_address_command = UpdateUserAddressCommand(
                user_id=user_id,
                address_id=address_id,
                street=data.get('street'),
                city=data.get('city'),
                country=data.get('country'),
            )
            
            command_bus = current_app.container.command_bus()
            command_bus.dispatch(update_address_command)
            
            # Devolver la dirección actualizada
            query = GetUserByIdQuery(id=user_id)
            query_bus = current_app.container.query_bus()
            user = query_bus.dispatch(query)
            
            addresses = user.get("addresses", [])
            updated_address = next(
                (addr for addr in addresses if addr.get("id") == address_id),
                None
            )
            
            return ControllerBase.format_response(updated_address, 200)

        except ValueError as e:
            if "not found" in str(e):
                return ControllerBase.format_response(
                    {"error": str(e)},
                    404
                )
            return AdminUserController._handle_error(e)
        except Exception as e:
            return AdminUserController._handle_error(e)
    
    @admin_user_controller.route('/<user_id>/addresses/<address_id>', methods=['DELETE'])
    def delete_user_address(user_id: str, address_id: str):
        """Elimina una dirección de un usuario."""
        try:
            remove_address_command = RemoveUserAddressCommand(
                user_id=user_id,
                address_id=address_id,
            )
            
            command_bus = current_app.container.command_bus()
            command_bus.dispatch(remove_address_command)
            
            return '', 204

        except ValueError as e:
            if "not found" in str(e):
                return ControllerBase.format_response(
                    {"error": str(e)},
                    404
                )
            return AdminUserController._handle_error(e)
        except Exception as e:
            return AdminUserController._handle_error(e)
    
    @staticmethod
    def _handle_error(e: Exception):
        """Maneja errores de forma centralizada."""
        status_code = 500
        if hasattr(e, 'code') and isinstance(e.code, int) and 100 <= e.code < 600:
            status_code = e.code
        
        return ControllerBase.format_response(
            {
                "error": str(e),
                "traceback": traceback.format_exc()
            },
            status_code
        )