"""
Projection que escucha eventos de dominio y actualiza modelos de lectura.
Implementa eventual consistency en CQRS.
"""

from Domain.HelloWorld.Events.HelloWorldCreated import HelloWorldCreated
from Domain.HelloWorld.Events.HelloWorldDeleted import HelloWorldDeleted
from Shared.Domain.Events.DomainEventSubscriber import DomainEventSubscriber
from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel
from config.log import logger


class HelloWorldProjection(DomainEventSubscriber):
    """
    Proyección que mantiene sincronizados los modelos de lectura.
    
    Escucha eventos de dominio y actualiza el read model correspondiente.
    Esto permite tener modelos de lectura optimizados separados del write model.
    """
    
    def __init__(self, read_repository=None):
        """
        Args:
            read_repository: Repositorio de lectura (opcional para logging)
        """
        self.read_repository = read_repository
    
    def subscribed_to(self) -> list:
        """
        Define los eventos a los que está suscrito.
        
        Returns:
            list: Lista de clases de eventos
        """
        return [HelloWorldCreated, HelloWorldDeleted]
    
    def handle(self, event) -> None:
        """
        Maneja eventos de dominio.
        
        Args:
            event: Evento de dominio a procesar
        """
        if isinstance(event, HelloWorldCreated):
            self._on_hello_world_created(event)
        elif isinstance(event, HelloWorldDeleted):
            self._on_hello_world_deleted(event)
    
    def _on_hello_world_created(self, event: HelloWorldCreated) -> None:
        """
        Procesa el evento de creación.
        Actualiza o crea el read model correspondiente.
        
        Args:
            event: Evento HelloWorldCreated
        """
        logger.info(
            f"[Projection] Sincronizando read model para HelloWorld creado "
            f"(ID: {event.hello_world_id})"
        )
        
        # Aquí podrías:
        # 1. Insertar en una tabla optimizada para lectura
        # 2. Actualizar caché (Redis, Memcached)
        # 3. Indexar en Elasticsearch
        # 4. Guardar en MongoDB para queries complejas
        
        # Ejemplo básico (si tienes read_repository):
        if self.read_repository:
            read_model = HelloWorldReadModel(
                id=event.hello_world_id,
                greeting=event.greeting,
                created_at=event.occurred_on
            )
            # self.read_repository.save(read_model)
            logger.debug(f"Read model creado: {read_model}")
    
    def _on_hello_world_deleted(self, event: HelloWorldDeleted) -> None:
        """
        Procesa el evento de eliminación.
        Elimina el read model correspondiente.
        
        Args:
            event: Evento HelloWorldDeleted
        """
        logger.info(
            f"[Projection] Eliminando read model para HelloWorld "
            f"(ID: {event.hello_world_id})"
        )
        
        # Aquí podrías:
        # 1. Eliminar de tabla de lectura
        # 2. Invalidar caché
        # 3. Eliminar de índices
        
        # Ejemplo básico:
        if self.read_repository:
            # self.read_repository.delete(event.hello_world_id)
            logger.debug(f"Read model eliminado: {event.hello_world_id}")
