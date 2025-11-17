"""
Tests unitarios para Domain Events y Event Dispatcher.
"""

import pytest
from unittest.mock import Mock
from Shared.Domain.Events.DomainEvent import DomainEvent
from Shared.Domain.Events.DomainEventSubscriber import DomainEventSubscriber
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher
from Domain.HelloWorld.Events.HelloWorldCreated import HelloWorldCreated
from Domain.HelloWorld.Events.HelloWorldDeleted import HelloWorldDeleted


class TestHelloWorldCreatedEvent:
    """Tests para el evento HelloWorldCreated."""
    
    def test_create_event_with_valid_data(self):
        """Debería crear un evento con datos válidos."""
        # Arrange & Act
        event = HelloWorldCreated(hello_world_id=123, greeting="Hello World")
        
        # Assert
        assert event.hello_world_id == 123
        assert event.greeting == "Hello World"
        assert event.event_name == "HelloWorldCreated"
        assert event.event_id is not None
        assert event.occurred_on is not None
    
    def test_event_to_dict_contains_all_data(self):
        """to_dict() debería incluir todos los datos."""
        # Arrange
        event = HelloWorldCreated(hello_world_id=456, greeting="Test")
        
        # Act
        event_dict = event.to_dict()
        
        # Assert
        assert event_dict['event_name'] == "HelloWorldCreated"
        assert event_dict['hello_world_id'] == 456
        assert event_dict['greeting'] == "Test"
        assert 'event_id' in event_dict
        assert 'occurred_on' in event_dict
    
    def test_two_events_have_different_ids(self):
        """Dos eventos deberían tener IDs únicos."""
        # Arrange & Act
        event1 = HelloWorldCreated(hello_world_id=1, greeting="Hello")
        event2 = HelloWorldCreated(hello_world_id=1, greeting="Hello")
        
        # Assert
        assert event1.event_id != event2.event_id
    
    def test_event_repr(self):
        """__repr__ debería ser informativo."""
        # Arrange
        event = HelloWorldCreated(hello_world_id=999, greeting="Test")
        
        # Act
        repr_string = repr(event)
        
        # Assert
        assert "HelloWorldCreated" in repr_string
        assert "999" in repr_string


class TestHelloWorldDeletedEvent:
    """Tests para el evento HelloWorldDeleted."""
    
    def test_create_deleted_event(self):
        """Debería crear un evento de eliminación."""
        # Arrange & Act
        event = HelloWorldDeleted(hello_world_id=789)
        
        # Assert
        assert event.hello_world_id == 789
        assert event.event_name == "HelloWorldDeleted"
    
    def test_deleted_event_to_dict(self):
        """to_dict() debería incluir el ID."""
        # Arrange
        event = HelloWorldDeleted(hello_world_id=321)
        
        # Act
        event_dict = event.to_dict()
        
        # Assert
        assert event_dict['hello_world_id'] == 321
        assert event_dict['event_name'] == "HelloWorldDeleted"


class TestEventDispatcher:
    """Tests para el EventDispatcher."""
    
    def test_subscribe_handler_to_event(self):
        """Debería permitir suscribir un handler a un evento."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_handler = Mock(spec=DomainEventSubscriber)
        mock_handler.subscribed_to.return_value = HelloWorldCreated
        
        # Act
        dispatcher.subscribe(mock_handler)
        
        # Assert
        assert dispatcher.has_subscribers(HelloWorldCreated)
        subscribers = dispatcher.get_subscribers(HelloWorldCreated)
        assert mock_handler in subscribers
    
    def test_publish_event_calls_subscribed_handlers(self):
        """Publicar un evento debería llamar a los handlers suscritos."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_handler = Mock(spec=DomainEventSubscriber)
        mock_handler.subscribed_to.return_value = HelloWorldCreated
        
        dispatcher.subscribe(mock_handler)
        event = HelloWorldCreated(hello_world_id=1, greeting="Test")
        
        # Act
        dispatcher.publish(event)
        
        # Assert
        mock_handler.handle.assert_called_once_with(event)
    
    def test_publish_event_does_not_call_unsubscribed_handlers(self):
        """No debería llamar handlers de otros eventos."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_handler_created = Mock(spec=DomainEventSubscriber)
        mock_handler_created.subscribed_to.return_value = HelloWorldCreated
        
        mock_handler_deleted = Mock(spec=DomainEventSubscriber)
        mock_handler_deleted.subscribed_to.return_value = HelloWorldDeleted
        
        dispatcher.subscribe(mock_handler_created)
        dispatcher.subscribe(mock_handler_deleted)
        
        event = HelloWorldCreated(hello_world_id=1, greeting="Test")
        
        # Act
        dispatcher.publish(event)
        
        # Assert
        mock_handler_created.handle.assert_called_once()
        mock_handler_deleted.handle.assert_not_called()
    
    def test_publish_multiple_events(self):
        """Debería publicar múltiples eventos en orden."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_handler = Mock(spec=DomainEventSubscriber)
        mock_handler.subscribed_to.return_value = HelloWorldCreated
        
        dispatcher.subscribe(mock_handler)
        
        events = [
            HelloWorldCreated(hello_world_id=1, greeting="First"),
            HelloWorldCreated(hello_world_id=2, greeting="Second")
        ]
        
        # Act
        dispatcher.publish_multiple(events)
        
        # Assert
        assert mock_handler.handle.call_count == 2
    
    def test_handler_exception_does_not_stop_other_handlers(self):
        """Una excepción en un handler no debería detener otros."""
        # Arrange
        dispatcher = EventDispatcher()
        
        failing_handler = Mock(spec=DomainEventSubscriber)
        failing_handler.subscribed_to.return_value = HelloWorldCreated
        failing_handler.handle.side_effect = Exception("Handler error")
        
        working_handler = Mock(spec=DomainEventSubscriber)
        working_handler.subscribed_to.return_value = HelloWorldCreated
        
        dispatcher.subscribe(failing_handler)
        dispatcher.subscribe(working_handler)
        
        event = HelloWorldCreated(hello_world_id=1, greeting="Test")
        
        # Act
        dispatcher.publish(event)
        
        # Assert
        failing_handler.handle.assert_called_once()
        working_handler.handle.assert_called_once()
    
    def test_no_subscribers_for_event(self):
        """Debería manejar eventos sin suscriptores."""
        # Arrange
        dispatcher = EventDispatcher()
        event = HelloWorldCreated(hello_world_id=1, greeting="Test")
        
        # Act & Assert (no debería lanzar excepción)
        dispatcher.publish(event)
        assert not dispatcher.has_subscribers(HelloWorldCreated)
    
    def test_clear_subscribers(self):
        """clear_subscribers debería eliminar todos los handlers."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_handler = Mock(spec=DomainEventSubscriber)
        mock_handler.subscribed_to.return_value = HelloWorldCreated
        
        dispatcher.subscribe(mock_handler)
        assert dispatcher.has_subscribers(HelloWorldCreated)
        
        # Act
        dispatcher.clear_subscribers()
        
        # Assert
        assert not dispatcher.has_subscribers(HelloWorldCreated)
    
    def test_subscribe_same_handler_twice_only_calls_once(self):
        """Suscribir el mismo handler dos veces no debería duplicarlo."""
        # Arrange
        dispatcher = EventDispatcher()
        mock_handler = Mock(spec=DomainEventSubscriber)
        mock_handler.subscribed_to.return_value = HelloWorldCreated
        
        # Act
        dispatcher.subscribe(mock_handler)
        dispatcher.subscribe(mock_handler)  # Segunda vez
        
        event = HelloWorldCreated(hello_world_id=1, greeting="Test")
        dispatcher.publish(event)
        
        # Assert
        subscribers = dispatcher.get_subscribers(HelloWorldCreated)
        assert len(subscribers) == 1
        mock_handler.handle.assert_called_once()
