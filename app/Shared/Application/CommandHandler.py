from abc import ABC, abstractmethod
from typing import Any


class CommandHandler(ABC):
    """
    Interfaz base para todos los Command Handlers.
    Asegura que implementen el método handle.
    """

    @abstractmethod
    def handle(self, command: Any) -> Any:
        """
        Maneja la ejecución de un comando.

        Args:
            command: El comando a ejecutar

        Returns:
            El resultado de la operación (opcional)
        """
        pass
