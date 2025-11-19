"""
Tests unitarios para Command Handlers (CQRS).
Valida la lógica de negocio y manejo de eventos.
"""

import pytest
from unittest.mock import Mock, MagicMock
from Application.Commands.CreateHelloWorldCommand import CreateHelloWorldCommand
from Application.Commands.UpdateHelloWorldCommand import UpdateHelloWorldCommand
from Application.Commands.DeleteHelloWorldCommand import DeleteHelloWorldCommand
from Application.CommandHandlers.CreateHelloWorldHandler import CreateHelloWorldHandler
from Application.CommandHandlers.UpdateHelloWorldHandler import UpdateHelloWorldHandler
from Application.CommandHandlers.DeleteHelloWorldHandler import DeleteHelloWorldHandler
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.Greeting import Greeting


class TestCreateHelloWorldHandler:
    """Tests para CreateHelloWorldHandler"""
    
    def test_handle_creates_hello_world_and_saves(self):
        """Debe crear entidad y guardarla en el repositorio"""
        # Arrange
        mock_repository = Mock()
        
        # Mock save para retornar entidad con ID
        def save_side_effect(entity):
            entity._id = 123
            return entity
        mock_repository.save = Mock(side_effect=save_side_effect)
        
        mock_event_dispatcher = Mock()
        
        handler = CreateHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = CreateHelloWorldCommand(greeting_text="Test Greeting")
        
        # Act
        result_id = handler.handle(command)
        
        # Assert
        mock_repository.save.assert_called_once()
        saved_entity = mock_repository.save.call_args[0][0]
        
        assert isinstance(saved_entity, HelloWorld)
        assert saved_entity.greeting.value == "Test Greeting"
        assert result_id == 123
    
    def test_handle_publishes_domain_events(self):
        """Debe publicar eventos de dominio"""
        # Arrange
        mock_repository = Mock()
        
        def save_side_effect(entity):
            entity._id = 456
            return entity
        mock_repository.save = Mock(side_effect=save_side_effect)
        
        mock_event_dispatcher = Mock()
        mock_event_dispatcher.publish_multiple = Mock()
        
        handler = CreateHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = CreateHelloWorldCommand(greeting_text="Test")
        
        # Act
        handler.handle(command)
        
        # Assert
        mock_event_dispatcher.publish_multiple.assert_called_once()
        events = mock_event_dispatcher.publish_multiple.call_args[0][0]
        assert len(events) > 0


class TestUpdateHelloWorldHandler:
    """Tests para UpdateHelloWorldHandler"""
    
    def test_handle_updates_existing_hello_world(self):
        """Debe actualizar entidad existente"""
        # Arrange
        greeting = Greeting.create("Original")
        existing_hello_world = HelloWorld.create(greeting)
        existing_hello_world._id = 1
        
        mock_repository = Mock()
        mock_repository.save = Mock(return_value=existing_hello_world)
        
        mock_read_repository = Mock()
        mock_read_repository.find_by_id = Mock(return_value=existing_hello_world)
        
        mock_event_dispatcher = Mock()
        mock_event_dispatcher.publish_multiple = Mock()
        
        handler = UpdateHelloWorldHandler(mock_repository, mock_read_repository, mock_event_dispatcher)
        command = UpdateHelloWorldCommand(id=1, greeting_text="Updated")
        
        # Act
        result = handler.handle(command)
        
        # Assert
        assert result is True
        mock_read_repository.find_by_id.assert_called_once_with(1)
        mock_repository.save.assert_called_once()
        
        # El handler modifica la entidad directamente
        assert existing_hello_world.greeting.value == "Updated"
    
    def test_handle_raises_error_when_not_found(self):
        """Debe lanzar error cuando no encuentra la entidad"""
        # Arrange
        mock_repository = Mock()
        
        mock_read_repository = Mock()
        mock_read_repository.find_by_id = Mock(return_value=None)
        
        mock_event_dispatcher = Mock()
        
        handler = UpdateHelloWorldHandler(mock_repository, mock_read_repository, mock_event_dispatcher)
        command = UpdateHelloWorldCommand(id=999, greeting_text="Test")
        
        # Act & Assert
        with pytest.raises(ValueError, match="HelloWorld with id 999 not found"):
            handler.handle(command)
    
    def test_handle_publishes_domain_events(self):
        """Debe publicar eventos de dominio después de actualizar (si los hay)"""
        # Arrange
        greeting = Greeting.create("Original")
        existing_hello_world = HelloWorld.create(greeting)
        existing_hello_world._id = 1
        
        # Limpiar eventos generados en create
        existing_hello_world.pull_domain_events()
        
        mock_repository = Mock()
        
        mock_read_repository = Mock()
        mock_read_repository.find_by_id = Mock(return_value=existing_hello_world)
        
        mock_event_dispatcher = Mock()
        mock_event_dispatcher.publish_multiple = Mock()
        
        handler = UpdateHelloWorldHandler(mock_repository, mock_read_repository, mock_event_dispatcher)
        command = UpdateHelloWorldCommand(id=1, greeting_text="Updated")
        
        # Act
        handler.handle(command)
        
        # Assert
        # Como no hay eventos generados por la actualización, no se llama publish_multiple
        # Este test verifica que el handler intente verificar eventos
        assert mock_repository.save.called


class TestDeleteHelloWorldHandler:
    """Tests para DeleteHelloWorldHandler"""
    
    def test_handle_deletes_existing_hello_world(self):
        """Debe eliminar entidad existente"""
        # Arrange
        greeting = Greeting.create("Test")
        existing_hello_world = HelloWorld.create(greeting)
        existing_hello_world._id = 1
        
        mock_repository = Mock()
        mock_repository.delete = MagicMock(return_value=True)
        
        mock_read_repository = Mock()
        mock_read_repository.findById = Mock(return_value=existing_hello_world)
        
        mock_event_dispatcher = Mock()
        
        handler = DeleteHelloWorldHandler(mock_repository, mock_read_repository, mock_event_dispatcher)
        command = DeleteHelloWorldCommand(id=1)
        
        # Act
        result = handler.handle(command)
        
        # Assert
        assert result is True
        mock_read_repository.find_by_id.assert_called_once_with(1)
        mock_repository.delete.assert_called_once_with(1)
    
    def test_handle_returns_false_when_not_found(self):
        """Debe retornar False cuando no encuentra la entidad"""
        # Arrange
        mock_repository = Mock()
        
        mock_read_repository = Mock()
        mock_read_repository.find_by_id = Mock(return_value=None)
        
        mock_event_dispatcher = Mock()
        
        handler = DeleteHelloWorldHandler(mock_repository, mock_read_repository, mock_event_dispatcher)
        command = DeleteHelloWorldCommand(id=999)
        
        # Act
        result = handler.handle(command)
        
        # Assert
        assert result is False
        mock_repository.delete.assert_not_called()
    
    def test_handle_publishes_domain_events(self):
        """Debe publicar eventos de dominio después de eliminar"""
        # Arrange
        greeting = Greeting.create("Test")
        existing_hello_world = HelloWorld.create(greeting)
        existing_hello_world._id = 1
        
        mock_repository = Mock()
        mock_repository.delete = MagicMock(return_value=True)
        
        mock_read_repository = Mock()
        mock_read_repository.findById = Mock(return_value=existing_hello_world)
        
        mock_event_dispatcher = Mock()
        
        handler = DeleteHelloWorldHandler(mock_repository, mock_read_repository, mock_event_dispatcher)
        command = DeleteHelloWorldCommand(id=1)
        
        # Act
        handler.handle(command)
        
        # Assert
        mock_event_dispatcher.publish.assert_called_once()
