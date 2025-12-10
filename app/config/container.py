"""
Dependency Injection Container
Gestiona todas las dependencias de la aplicación usando dependency-injector.
Incluye soporte completo para CQRS con Command Bus y Query Bus.
"""

from dependency_injector import containers, providers
from Admin.Infrastructure.Repository.UserWriteRepository import UserWriteRepository

# CQRS - Command Bus y Query Bus
from Shared.Application.CommandBus import CommandBus
from Shared.Application.QueryBus import QueryBus

# Commands y Command Handlers
from Admin.Application.Commands.CreateUserCommand import CreateUserCommand
from Admin.Application.Commands.UpdateUserCommand import UpdateUserCommand
from Admin.Application.Commands.DeleteUserCommand import DeleteUserCommand
from Admin.Application.Commands.AddUserAddressCommand import AddUserAddressCommand
from Admin.Application.Commands.UpdateUserAddressCommand import UpdateUserAddressCommand
from Admin.Application.Commands.RemoveUserAddressCommand import RemoveUserAddressCommand

# Queries y Query Handlers
from Admin.Application.Queries.GetUserByIdQuery import GetUserByIdQuery
from Admin.Application.Queries.GetAllUsersQuery import GetAllUsersQuery

# Event System
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher
from Admin.Application.CommandHandlers.CreateUserHander import CreateUserHander
from Admin.Application.CommandHandlers.UpdateUserHandler import UpdateUserHandler
from Admin.Application.CommandHandlers.DeleteUserHandler import DeleteUserHandler
from Admin.Application.CommandHandlers.AddUserAddressHandler import AddUserAddressHandler
from Admin.Application.CommandHandlers.UpdateUserAddressHandler import UpdateUserAddressHandler
from Admin.Application.CommandHandlers.RemoveUserAddressHandler import RemoveUserAddressHandler
from Admin.Application.QueryHandlers.GetUserByIdHandler import GetUserByIdHandler
from Admin.Application.QueryHandlers.GetAllUsersHandler import GetAllUsersHandler
from Admin.Infrastructure.Repository.UserWriteRepository import UserWriteRepository
from Admin.Infrastructure.Repository.UserReadRepository import UserReadRepository


class Container(containers.DeclarativeContainer):
    """
    Contenedor de Inyección de Dependencias con soporte para CQRS.

    Define cómo crear e inyectar todas las dependencias:
    - Repositorios (Write y Read separados)
    - Command Bus y Query Bus
    - Command Handlers y Query Handlers
    - Event System (Dispatcher, Handlers, Projections)
    - Use Cases (legacy, para compatibilidad)
    """

    # Configuración
    config = providers.Configuration()

    # ========== EVENT SYSTEM ==========

    # Event Dispatcher (Singleton)
    event_dispatcher = providers.Singleton(
        EventDispatcher
    )

    # ========== REPOSITORIES ==========
  
    admin_user_write_repository = providers.Factory(
        UserWriteRepository
    )
    
    admin_user_read_repository = providers.Factory(
        UserReadRepository
    )


    # ========== CQRS - COMMAND HANDLERS ==========
 
    create_user_command_handler = providers.Factory(
        CreateUserHander,
        write_repository=admin_user_write_repository,
        event_dispatcher=event_dispatcher
    )
    
    update_user_command_handler = providers.Factory(
        UpdateUserHandler,
        write_repository=admin_user_write_repository,
        read_repository=admin_user_read_repository,
        event_dispatcher=event_dispatcher
    )
    
    delete_user_command_handler = providers.Factory(
        DeleteUserHandler,
        write_repository=admin_user_write_repository,
        event_dispatcher=event_dispatcher
    )
    
    add_user_address_command_handler = providers.Factory(
        AddUserAddressHandler,
        write_repository=admin_user_write_repository,
        event_dispatcher=event_dispatcher
    )
    
    update_user_address_command_handler = providers.Factory(
        UpdateUserAddressHandler,
        write_repository=admin_user_write_repository,
        event_dispatcher=event_dispatcher
    )
    
    remove_user_address_command_handler = providers.Factory(
        RemoveUserAddressHandler,
        write_repository=admin_user_write_repository,
        event_dispatcher=event_dispatcher
    )

    # ========== CQRS - QUERY HANDLERS ==========
   
    get_user_by_id_query_handler = providers.Factory(
        GetUserByIdHandler,
        read_repository=admin_user_read_repository
    )
    
    get_all_users_query_handler = providers.Factory(
        GetAllUsersHandler,
        read_repository=admin_user_read_repository
    )

    # ========== CQRS - BUSES ==========

    command_bus = providers.Singleton(
        CommandBus
    )

    query_bus = providers.Singleton(
        QueryBus
    )

def init_container(app) -> Container:
    """
    Inicializa el contenedor con la configuración de Flask.

    Args:
        app: Instancia de Flask

    Returns:
        Container configurado
    """
    container = Container()

    # Configurar valores desde Flask config
    container.config.stream_availability_host.from_value(
        app.config.get('STREAM_AVAILABILITY_HOST', '')
    )
    container.config.stream_availability_key.from_value(
        app.config.get('STREAM_AVAILABILITY_KEY', '')
    )

    # Registrar event handlers en el dispatcher
    _register_event_handlers(container)

    # Registrar command handlers en el command bus
    _register_command_handlers(container)

    # Registrar query handlers en el query bus
    _register_query_handlers(container)

    return container


def _register_event_handlers(container: Container) -> None:
    """
    Registra todos los event handlers en el event dispatcher.

    Args:
        container: El container con las dependencias
    """
    dispatcher = container.event_dispatcher()




def _register_command_handlers(container: Container) -> None:
    """
    Registra todos los command handlers en el command bus.

    Args:
        container: El container con las dependencias
    """
    command_bus = container.command_bus()

    # Registrar handlers de comandos
    command_bus.register(
        CreateUserCommand,
        container.create_user_command_handler()
    )
    command_bus.register(
        UpdateUserCommand,
        container.update_user_command_handler()
    )
    command_bus.register(
        DeleteUserCommand,
        container.delete_user_command_handler()
    )
    command_bus.register(
        AddUserAddressCommand,
        container.add_user_address_command_handler()
    )
    command_bus.register(
        UpdateUserAddressCommand,
        container.update_user_address_command_handler()
    )
    command_bus.register(
        RemoveUserAddressCommand,
        container.remove_user_address_command_handler()
    )


def _register_query_handlers(container: Container) -> None:
    """
    Registra todos los query handlers en el query bus.

    Args:
        container: El container con las dependencias
    """
    query_bus = container.query_bus()

    # Registrar handlers de queries
    query_bus.register(
        GetUserByIdQuery,
        container.get_user_by_id_query_handler()
    )
    query_bus.register(
        GetAllUsersQuery,
        container.get_all_users_query_handler()
    )
