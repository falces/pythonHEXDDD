from typing import List
from Shared.Domain.Events.DomainEvent import DomainEvent


class EntityBase:
    """
    Clase base para todas las entidades del dominio.
    Las entidades tienen identidad y ciclo de vida.
    """
    pass


class AggregateRootBase(EntityBase):
    """
    Clase base para los Aggregate Roots.
    
    Un Aggregate Root es la entidad raíz de un agregado que:
    - Garantiza la consistencia del agregado
    - Controla el acceso al agregado desde el exterior
    - Gestiona los eventos de dominio del agregado
    """
    
    def __init__(self):
        self._domain_events: List[DomainEvent] = []
    
    def record_event(self, event: DomainEvent) -> None:
        """
        Registra un evento de dominio en el agregado.
        
        Los eventos se acumulan hasta que sean extraídos
        por el dispatcher para ser publicados.
        
        Args:
            event: El evento de dominio a registrar
        """
        self._domain_events.append(event)
    
    def pull_domain_events(self) -> List[DomainEvent]:
        """
        Extrae y limpia los eventos de dominio acumulados.
        
        Este método es llamado típicamente después de persistir
        el agregado, para publicar los eventos.
        
        Returns:
            List[DomainEvent]: Lista de eventos acumulados
        """
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events
    
    def clear_events(self) -> None:
        """
        Limpia todos los eventos sin retornarlos.
        Útil para casos de rollback o testing.
        """
        self._domain_events.clear()
    
    @property
    def has_events(self) -> bool:
        """
        Verifica si el agregado tiene eventos pendientes.
        
        Returns:
            bool: True si hay eventos, False en caso contrario
        """
        return len(self._domain_events) > 0