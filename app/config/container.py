"""
Dependency Injection Container
Gestiona todas las dependencias de la aplicación usando dependency-injector.
"""

from dependency_injector import containers, providers
from Infrastructure.Repository.HelloWorldRepository import HelloWorldRepository
from Infrastructure.Repository.ShowsRepository import ShowsRepository
from Application.HelloWorldService import HelloWorldService
from Application.MoviesService import MoviesService

# Use Cases - HelloWorld
from Application.UseCases.HelloWorld.CreateHelloWorldUseCase import CreateHelloWorldUseCase
from Application.UseCases.HelloWorld.GetAllHelloWorldUseCase import GetAllHelloWorldUseCase
from Application.UseCases.HelloWorld.GetHelloWorldByIdUseCase import GetHelloWorldByIdUseCase
from Application.UseCases.HelloWorld.DeleteHelloWorldUseCase import DeleteHelloWorldUseCase

# Use Cases - Shows
from Application.UseCases.Shows.SearchShowsUseCase import SearchShowsUseCase
from Application.UseCases.Shows.GetShowByIdUseCase import GetShowByIdUseCase

# Event System
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher
from Application.EventHandlers.HelloWorldCreatedLogger import HelloWorldCreatedLogger
from Application.EventHandlers.HelloWorldDeletedLogger import HelloWorldDeletedLogger


class Container(containers.DeclarativeContainer):
    """
    Contenedor de Inyección de Dependencias.
    
    Define cómo crear e inyectar todas las dependencias de la aplicación:
    - Repositorios
    - Servicios
    - Use Cases
    - Event System (Dispatcher y Handlers)
    """
    
    # Configuración
    config = providers.Configuration()
    
    # ========== EVENT SYSTEM ==========
    
    # Event Dispatcher (Singleton - una única instancia en toda la app)
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
    
    # HelloWorld Repository (SQLAlchemy)
    hello_world_repository = providers.Factory(
        HelloWorldRepository
    )
    
    # Shows Repository (API Externa)
    shows_repository = providers.Factory(
        ShowsRepository,
        api_host=config.stream_availability_host,
        api_key=config.stream_availability_key
    )
    
    # ========== SERVICES ==========
    
    # Movies Service
    movies_service = providers.Factory(
        MoviesService,
        repository=shows_repository
    )
    
    # ========== USE CASES - HELLO WORLD ==========
    
    create_hello_world_use_case = providers.Factory(
        CreateHelloWorldUseCase,
        repository=hello_world_repository,
        event_dispatcher=event_dispatcher
    )
    
    get_all_hello_world_use_case = providers.Factory(
        GetAllHelloWorldUseCase,
        repository=hello_world_repository
    )
    
    get_hello_world_by_id_use_case = providers.Factory(
        GetHelloWorldByIdUseCase,
        repository=hello_world_repository
    )
    
    delete_hello_world_use_case = providers.Factory(
        DeleteHelloWorldUseCase,
        repository=hello_world_repository,
        event_dispatcher=event_dispatcher
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
    
    return container


def _register_event_handlers(container: Container) -> None:
    """
    Registra todos los event handlers en el event dispatcher.
    
    Esta función se ejecuta al inicializar el container y suscribe
    todos los handlers a sus eventos correspondientes.
    
    Args:
        container: El container con las dependencias
    """
    dispatcher = container.event_dispatcher()
    
    # Suscribir handlers de HelloWorld
    dispatcher.subscribe(container.hello_world_created_logger())
    dispatcher.subscribe(container.hello_world_deleted_logger())
    
    # Aquí se pueden agregar más handlers en el futuro:
    # dispatcher.subscribe(container.send_email_on_hello_world_created())
    # dispatcher.subscribe(container.update_stats_on_hello_world_deleted())
    # etc.
