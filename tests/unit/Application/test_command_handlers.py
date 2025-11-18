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
        mock_repository.save = MagicMock()
        mock_event_dispatcher = Mock()
        
        handler = CreateHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = CreateHelloWorldCommand(greeting="Test Greeting")
        
        # Act
        result_id = handler.handle(command)
        
        # Assert
        mock_repository.save.assert_called_once()
        saved_entity = mock_repository.save.call_args[0][0]
        
        assert isinstance(saved_entity, HelloWorld)
        assert saved_entity.greeting.value == "Test Greeting"
        assert isinstance(result_id, int)
    
    def test_handle_publishes_domain_events(self):
        """Debe publicar eventos de dominio"""
        # Arrange
        mock_repository = Mock()
        mock_event_dispatcher = Mock()
        
        handler = CreateHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = CreateHelloWorldCommand(greeting="Test")
        
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
        mock_repository.find_by_id = Mock(return_value=existing_hello_world)
        mock_repository.save = MagicMock()
        mock_event_dispatcher = Mock()
        
        handler = UpdateHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = UpdateHelloWorldCommand(id=1, greeting="Updated")
        
        # Act
        result = handler.handle(command)
        
        # Assert
        assert result is True
        mock_repository.find_by_id.assert_called_once_with(1)
        mock_repository.save.assert_called_once()
        
        saved_entity = mock_repository.save.call_args[0][0]
        assert saved_entity.greeting.value == "Updated"
    
    def test_handle_raises_error_when_not_found(self):
        """Debe lanzar error cuando no encuentra la entidad"""
        # Arrange
        mock_repository = Mock()
        mock_repository.find_by_id = Mock(return_value=None)
        mock_event_dispatcher = Mock()
        
        handler = UpdateHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = UpdateHelloWorldCommand(id=999, greeting="Test")
        
        # Act & Assert
        with pytest.raises(ValueError, match="HelloWorld con ID 999 no encontrado"):
            handler.handle(command)
    
    def test_handle_publishes_domain_events(self):
        """Debe publicar eventos de dominio después de actualizar"""
        # Arrange
        greeting = Greeting.create("Original")
        existing_hello_world = HelloWorld.create(greeting)
        existing_hello_world._id = 1
        
        mock_repository = Mock()
        mock_repository.find_by_id = Mock(return_value=existing_hello_world)
        mock_event_dispatcher = Mock()
        
        handler = UpdateHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = UpdateHelloWorldCommand(id=1, greeting="Updated")
        
        # Act
        handler.handle(command)
        
        # Assert
        mock_event_dispatcher.publish_multiple.assert_called_once()


class TestDeleteHelloWorldHandler:
    """Tests para DeleteHelloWorldHandler"""
    
    def test_handle_deletes_existing_hello_world(self):
        """Debe eliminar entidad existente"""
        # Arrange
        greeting = Greeting.create("Test")
        existing_hello_world = HelloWorld.create(greeting)
        existing_hello_world._id = 1
        
        mock_repository = Mock()
        mock_repository.find_by_id = Mock(return_value=existing_hello_world)
        mock_repository.delete = MagicMock()
        mock_event_dispatcher = Mock()
        
        handler = DeleteHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = DeleteHelloWorldCommand(id=1)
        
        # Act
        result = handler.handle(command)
        
        # Assert
        assert result is True
        mock_repository.find_by_id.assert_called_once_with(1)
        mock_repository.delete.assert_called_once_with(1)
    
    def test_handle_raises_error_when_not_found(self):
        """Debe lanzar error cuando no encuentra la entidad"""
        # Arrange
        mock_repository = Mock()
        mock_repository.find_by_id = Mock(return_value=None)
        mock_event_dispatcher = Mock()
        
        handler = DeleteHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = DeleteHelloWorldCommand(id=999)
        
        # Act & Assert
        with pytest.raises(ValueError, match="HelloWorld con ID 999 no encontrado"):
            handler.handle(command)
    
    def test_handle_publishes_domain_events(self):
        """Debe publicar eventos de dominio después de eliminar"""
        # Arrange
        greeting = Greeting.create("Test")
        existing_hello_world = HelloWorld.create(greeting)
        existing_hello_world._id = 1
        
        mock_repository = Mock()
        mock_repository.find_by_id = Mock(return_value=existing_hello_world)
        mock_event_dispatcher = Mock()
        
        handler = DeleteHelloWorldHandler(mock_repository, mock_event_dispatcher)
        command = DeleteHelloWorldCommand(id=1)
        
        # Act
        handler.handle(command)
        
        # Assert
        mock_event_dispatcher.publish_multiple.assert_called_once()
