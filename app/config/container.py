"""
Dependency Injection Container
Gestiona todas las dependencias de la aplicación usando dependency-injector.
Incluye soporte completo para CQRS con Command Bus y Query Bus.
"""

from dependency_injector import containers, providers
from Infrastructure.Repository.HelloWorldWriteRepository import HelloWorldWriteRepository
from Infrastructure.Repository.HelloWorldReadRepository import HelloWorldReadRepository
from Infrastructure.Repository.ShowsAPIRepository import ShowsAPIRepository
from Application.MoviesService import MoviesService

# CQRS - Command Bus y Query Bus
from Shared.Application.CommandBus import CommandBus
from Shared.Application.QueryBus import QueryBus

# Commands y Command Handlers
from Application.Commands.CreateHelloWorldCommand import CreateHelloWorldCommand
from Application.Commands.UpdateHelloWorldCommand import UpdateHelloWorldCommand
from Application.Commands.DeleteHelloWorldCommand import DeleteHelloWorldCommand
from Application.CommandHandlers.CreateHelloWorldHandler import CreateHelloWorldHandler
from Application.CommandHandlers.UpdateHelloWorldHandler import UpdateHelloWorldHandler
from Application.CommandHandlers.DeleteHelloWorldHandler import DeleteHelloWorldHandler

# Queries y Query Handlers
from Application.Queries.GetAllHelloWorldQuery import GetAllHelloWorldQuery
from Application.Queries.GetHelloWorldByIdQuery import GetHelloWorldByIdQuery
from Application.Queries.SearchHelloWorldQuery import SearchHelloWorldQuery
from Application.QueryHandlers.GetAllHelloWorldHandler import GetAllHelloWorldHandler
from Application.QueryHandlers.GetHelloWorldByIdHandler import GetHelloWorldByIdHandler
from Application.QueryHandlers.SearchHelloWorldHandler import SearchHelloWorldHandler

# Use Cases - Shows
from Application.UseCases.Shows.SearchShowsUseCase import SearchShowsUseCase
from Application.UseCases.Shows.GetShowByIdUseCase import GetShowByIdUseCase

# Event System
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher
from Application.EventHandlers.HelloWorldCreatedLogger import HelloWorldCreatedLogger
from Application.EventHandlers.HelloWorldDeletedLogger import HelloWorldDeletedLogger
from Infrastructure.Projections.HelloWorldProjection import HelloWorldProjection


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

    # Event Handlers
    hello_world_created_logger = providers.Factory(
        HelloWorldCreatedLogger
    )

    hello_world_deleted_logger = providers.Factory(
        HelloWorldDeletedLogger
    )

    # ========== REPOSITORIES ==========

    # Write Repository (para comandos)
    hello_world_write_repository = providers.Factory(
        HelloWorldWriteRepository
    )

    # Read Repository (para queries)
    hello_world_read_repository = providers.Factory(
        HelloWorldReadRepository
    )

    # Shows Repository (API Externa)
    shows_repository = providers.Factory(
        ShowsAPIRepository,
        api_host=config.stream_availability_host,
        api_key=config.stream_availability_key
    )

    # ========== CQRS - COMMAND HANDLERS ==========

    create_hello_world_command_handler = providers.Factory(
        CreateHelloWorldHandler,
        write_repository=hello_world_write_repository,
        event_dispatcher=event_dispatcher
    )

    update_hello_world_command_handler = providers.Factory(
        UpdateHelloWorldHandler,
        write_repository=hello_world_write_repository,
        read_repository=hello_world_read_repository,
        event_dispatcher=event_dispatcher
    )

    delete_hello_world_command_handler = providers.Factory(
        DeleteHelloWorldHandler,
        write_repository=hello_world_write_repository,
        read_repository=hello_world_read_repository,
        event_dispatcher=event_dispatcher
    )

    # ========== CQRS - QUERY HANDLERS ==========

    get_all_hello_world_query_handler = providers.Factory(
        GetAllHelloWorldHandler,
        read_repository=hello_world_read_repository
    )

    get_hello_world_by_id_query_handler = providers.Factory(
        GetHelloWorldByIdHandler,
        read_repository=hello_world_read_repository
    )

    search_hello_world_query_handler = providers.Factory(
        SearchHelloWorldHandler,
        read_repository=hello_world_read_repository
    )

    # ========== CQRS - BUSES ==========

    command_bus = providers.Singleton(
        CommandBus
    )

    query_bus = providers.Singleton(
        QueryBus
    )

    # ========== PROJECTIONS ==========

    hello_world_projection = providers.Factory(
        HelloWorldProjection,
        read_repository=hello_world_read_repository
    )

    # ========== SERVICES ==========

    # Movies Service
    movies_service = providers.Factory(
        MoviesService,
        repository=shows_repository
    )

    # ========== USE CASES - SHOWS ==========

    search_shows_use_case = providers.Factory(
        SearchShowsUseCase,
        repository=shows_repository
    )

    get_show_by_id_use_case = providers.Factory(
        GetShowByIdUseCase,
        repository=shows_repository
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

    # Suscribir handlers de HelloWorld
    dispatcher.subscribe(container.hello_world_created_logger())
    dispatcher.subscribe(container.hello_world_deleted_logger())

    # Suscribir projection para actualizar read models
    dispatcher.subscribe(container.hello_world_projection())


def _register_command_handlers(container: Container) -> None:
    """
    Registra todos los command handlers en el command bus.

    Args:
        container: El container con las dependencias
    """
    command_bus = container.command_bus()

    # Registrar handlers de comandos
    command_bus.register(
        CreateHelloWorldCommand,
        container.create_hello_world_command_handler()
    )
    command_bus.register(
        UpdateHelloWorldCommand,
        container.update_hello_world_command_handler()
    )
    command_bus.register(
        DeleteHelloWorldCommand,
        container.delete_hello_world_command_handler()
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
        GetAllHelloWorldQuery,
        container.get_all_hello_world_query_handler()
    )
    query_bus.register(
        GetHelloWorldByIdQuery,
        container.get_hello_world_by_id_query_handler()
    )
    query_bus.register(
        SearchHelloWorldQuery,
        container.search_hello_world_query_handler()
    )
