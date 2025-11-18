"""
Command Bus para despachar comandos a sus handlers.
Implementa el patrón Command Bus de CQRS.
"""

from typing import Dict, Type, Any


class CommandBus:
    """
    Bus de comandos que despacha comandos a sus handlers correspondientes.
    
    Separa la invocación de comandos de su ejecución.
    """
    
    def __init__(self):
        self._handlers: Dict[Type, Any] = {}
    
    def register(self, command_type: Type, handler: Any) -> None:
        """
        Registra un handler para un tipo de comando.
        
        Args:
            command_type: Clase del comando
            handler: Instancia del handler que procesará el comando
            
        Raises:
            ValueError: Si el comando ya tiene un handler registrado
        """
        if command_type in self._handlers:
            raise ValueError(f"Handler already registered for {command_type.__name__}")
        
        self._handlers[command_type] = handler
    
    def dispatch(self, command: Any) -> Any:
        """
        Despacha un comando a su handler correspondiente.
        
        Args:
            command: Instancia del comando a ejecutar
            
        Returns:
            El resultado del handler
            
        Raises:
            ValueError: Si no hay handler registrado para el comando
        """
        command_type = type(command)
        
        if command_type not in self._handlers:
            raise ValueError(f"No handler registered for command {command_type.__name__}")
        
        handler = self._handlers[command_type]
        return handler.handle(command)
    
    def has_handler(self, command_type: Type) -> bool:
        """
        Verifica si existe un handler para un tipo de comando.
        
        Args:
            command_type: Clase del comando
            
        Returns:
            bool: True si existe handler
        """
        return command_type in self._handlers
