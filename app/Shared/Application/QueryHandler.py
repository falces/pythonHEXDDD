from abc import ABC, abstractmethod
from typing import Any


class QueryHandler(ABC):
    """
    Interfaz base para todos los Query Handlers.
    Asegura que implementen el método handle.
    """

    @abstractmethod
    def handle(self, query: Any) -> Any:
        """
        Maneja la ejecución de una query.

        Args:
            query: La query a ejecutar

        Returns:
            El resultado de la consulta (ReadModels, listas, etc.)
        """
        pass
