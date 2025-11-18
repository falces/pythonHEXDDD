"""
Tests unitarios para CommandBus (CQRS).
Valida el registro y despacho de comandos.
"""

import pytest
from unittest.mock import Mock
from Shared.Application.CommandBus import CommandBus
from Application.Commands.CreateHelloWorldCommand import CreateHelloWorldCommand
from Application.Commands.DeleteHelloWorldCommand import DeleteHelloWorldCommand


class TestCommandBus:
    """Tests para CommandBus"""
    
    def test_register_and_dispatch_command(self):
        """Debe registrar handler y despachar comando correctamente"""
        # Arrange
        bus = CommandBus()
        mock_handler = Mock()
        mock_handler.handle = Mock(return_value=123)
        
        command = CreateHelloWorldCommand(greeting="Test")
        
        # Act
        bus.register(CreateHelloWorldCommand, mock_handler)
        result = bus.dispatch(command)
        
        # Assert
        assert result == 123
        mock_handler.handle.assert_called_once_with(command)
    
    def test_dispatch_raises_error_for_unregistered_command(self):
        """Debe lanzar error al despachar comando no registrado"""
        # Arrange
        bus = CommandBus()
        command = CreateHelloWorldCommand(greeting="Test")
        
        # Act & Assert
        with pytest.raises(ValueError, match="No hay handler registrado para"):
            bus.dispatch(command)
    
    def test_register_multiple_commands(self):
        """Debe permitir registrar múltiples tipos de comandos"""
        # Arrange
        bus = CommandBus()
        create_handler = Mock()
        delete_handler = Mock()
        
        create_command = CreateHelloWorldCommand(greeting="Test")
        delete_command = DeleteHelloWorldCommand(id=1)
        
        # Act
        bus.register(CreateHelloWorldCommand, create_handler)
        bus.register(DeleteHelloWorldCommand, delete_handler)
        
        bus.dispatch(create_command)
        bus.dispatch(delete_command)
        
        # Assert
        create_handler.handle.assert_called_once_with(create_command)
        delete_handler.handle.assert_called_once_with(delete_command)
    
    def test_register_replaces_existing_handler(self):
        """Debe reemplazar handler existente al re-registrar"""
        # Arrange
        bus = CommandBus()
        old_handler = Mock()
        new_handler = Mock()
        
        command = CreateHelloWorldCommand(greeting="Test")
        
        # Act
        bus.register(CreateHelloWorldCommand, old_handler)
        bus.register(CreateHelloWorldCommand, new_handler)
        bus.dispatch(command)
        
        # Assert
        old_handler.handle.assert_not_called()
        new_handler.handle.assert_called_once()
    
    def test_dispatch_propagates_handler_exceptions(self):
        """Debe propagar excepciones lanzadas por el handler"""
        # Arrange
        bus = CommandBus()
        mock_handler = Mock()
        mock_handler.handle = Mock(side_effect=RuntimeError("Handler error"))
        
        command = CreateHelloWorldCommand(greeting="Test")
        bus.register(CreateHelloWorldCommand, mock_handler)
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Handler error"):
            bus.dispatch(command)
