"""
Query Bus para despachar queries a sus handlers.
Implementa el patrón Query Bus de CQRS.
"""

from typing import Dict, Type, Any
from Shared.Application.QueryHandler import QueryHandler


class QueryBus:
    """
    Bus de queries que despacha queries a sus handlers correspondientes.

    Separa la invocación de queries de su ejecución.
    Usado exclusivamente para lecturas (no modifica estado).
    """

    def __init__(self):
        self._handlers: Dict[Type, QueryHandler] = {}

    def register(self, query_type: Type, handler: QueryHandler) -> None:
        """
        Registra un handler para un tipo de query.

        Args:
            query_type: Clase de la query
            handler: Instancia del handler que procesará la query

        Raises:
            ValueError: Si la query ya tiene un handler registrado
        """
        if query_type in self._handlers:
            raise ValueError(
                f"Handler already registered for {query_type.__name__}")

        self._handlers[query_type] = handler

    def dispatch(self, query: Any) -> Any:
        """
        Despacha una query a su handler correspondiente.

        Args:
            query: Instancia de la query a ejecutar

        Returns:
            El resultado del handler (ReadModels, listas, etc.)

        Raises:
            ValueError: Si no hay handler registrado para la query
        """
        query_type = type(query)

        if query_type not in self._handlers:
            raise ValueError(
                f"No handler registered for query {query_type.__name__}")

        handler = self._handlers[query_type]
        return handler.handle(query)

    def has_handler(self, query_type: Type) -> bool:
        """
        Verifica si existe un handler para un tipo de query.

        Args:
            query_type: Clase de la query

        Returns:
            bool: True si existe handler
        """
        return query_type in self._handlers
