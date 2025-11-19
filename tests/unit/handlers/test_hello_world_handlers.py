"""
Tests unitarios para los Event Handlers de HelloWorld.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from Domain.HelloWorld.Events.HelloWorldCreated import HelloWorldCreated
from Domain.HelloWorld.Events.HelloWorldDeleted import HelloWorldDeleted
from Application.EventHandlers.HelloWorldCreatedLogger import HelloWorldCreatedLogger
from Application.EventHandlers.HelloWorldDeletedLogger import HelloWorldDeletedLogger


class TestHelloWorldCreatedLogger:
    """Tests para HelloWorldCreatedLogger."""

    def test_handle_logs_creation_event(self):
        """Debería registrar el evento de creación."""
        # Arrange
        handler = HelloWorldCreatedLogger()
        event = HelloWorldCreated(
            hello_world_id=123,
            greeting="Test Greeting"
        )

        # Act & Assert - verificar que no lanza excepción
        with patch('Application.EventHandlers.HelloWorldCreatedLogger.logger') as mock_logger:
            handler.handle(event)
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "HelloWorld creado" in call_args
            assert "123" in call_args

    def test_handle_with_special_characters_in_greeting(self):
        """Debería manejar greetings con caracteres especiales."""
        # Arrange
        handler = HelloWorldCreatedLogger()
        event = HelloWorldCreated(
            hello_world_id=456,
            greeting="¡Hola Mundo! 你好世界"
        )

        # Act & Assert
        with patch('Application.EventHandlers.HelloWorldCreatedLogger.logger') as mock_logger:
            handler.handle(event)
            mock_logger.info.assert_called_once()

    def test_handle_with_none_greeting(self):
        """Debería manejar greeting None."""
        # Arrange
        handler = HelloWorldCreatedLogger()
        event = HelloWorldCreated(
            hello_world_id=789,
            greeting=None
        )

        # Act & Assert
        with patch('Application.EventHandlers.HelloWorldCreatedLogger.logger') as mock_logger:
            handler.handle(event)
            mock_logger.info.assert_called_once()


class TestHelloWorldDeletedLogger:
    """Tests para HelloWorldDeletedLogger."""

    def test_handle_logs_deletion_event(self):
        """Debería registrar el evento de eliminación."""
        # Arrange
        handler = HelloWorldDeletedLogger()
        event = HelloWorldDeleted(
            hello_world_id=123
        )

        # Act & Assert
        with patch('Application.EventHandlers.HelloWorldDeletedLogger.logger') as mock_logger:
            handler.handle(event)
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "HelloWorld eliminado" in call_args
            assert "123" in call_args

    def test_handle_with_numeric_id(self):
        """Debería manejar IDs numéricos correctamente."""
        # Arrange
        handler = HelloWorldDeletedLogger()
        event = HelloWorldDeleted(
            hello_world_id=999999
        )

        # Act & Assert
        with patch('Application.EventHandlers.HelloWorldDeletedLogger.logger') as mock_logger:
            handler.handle(event)
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "999999" in call_args

    def test_handle_with_empty_greeting(self):
        """Debería manejar eventos de eliminación correctamente."""
        # Arrange
        handler = HelloWorldDeletedLogger()
        event = HelloWorldDeleted(
            hello_world_id=111
        )

        # Act & Assert
        with patch('Application.EventHandlers.HelloWorldDeletedLogger.logger') as mock_logger:
            handler.handle(event)
            mock_logger.info.assert_called_once()


class TestHandlersIntegration:
    """Tests de integración entre handlers y eventos."""

    def test_multiple_handlers_can_process_same_event(self):
        """Múltiples handlers deberían poder procesar el mismo evento."""
        # Arrange
        handler1 = HelloWorldCreatedLogger()
        handler2 = HelloWorldCreatedLogger()  # Simular múltiples subscriptores

        event = HelloWorldCreated(
            hello_world_id=100,
            greeting="Multi Handler Test"
        )

        # Act & Assert
        with patch('Application.EventHandlers.HelloWorldCreatedLogger.logger'):
            handler1.handle(event)
            handler2.handle(event)
            # Ambos deberían procesar sin interferir

    def test_handler_does_not_mutate_event(self):
        """Handler no debería mutar el evento."""
        # Arrange
        handler = HelloWorldCreatedLogger()
        event = HelloWorldCreated(
            hello_world_id=200,
            greeting="Immutable Test"
        )
        original_id = event.hello_world_id
        original_greeting = event.greeting

        # Act
        with patch('Application.EventHandlers.HelloWorldCreatedLogger.logger'):
            handler.handle(event)

        # Assert
        assert event.hello_world_id == original_id
        assert event.greeting == original_greeting
