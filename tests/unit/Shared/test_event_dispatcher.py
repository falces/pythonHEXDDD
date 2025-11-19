"""
Tests unitarios para EventDispatcher.
Valida suscripción a uno o múltiples eventos y publicación.
"""

import pytest
from unittest.mock import Mock
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher
from Domain.HelloWorld.Events.HelloWorldCreated import HelloWorldCreated
from Domain.HelloWorld.Events.HelloWorldDeleted import HelloWorldDeleted
from datetime import datetime


class MockSingleEventSubscriber:
    """Mock de suscriptor a un solo evento"""

    def subscribed_to(self):
        return HelloWorldCreated

    def handle(self, event):
        pass


class MockMultipleEventSubscriber:
    """Mock de suscriptor a múltiples eventos"""

    def subscribed_to(self):
        return [HelloWorldCreated, HelloWorldDeleted]

    def handle(self, event):
        pass


class TestEventDispatcher:
    """Tests para EventDispatcher"""

    def test_subscribe_single_event(self):
        """Debe suscribir correctamente a un solo evento"""
        # Arrange
        dispatcher = EventDispatcher()
        subscriber = MockSingleEventSubscriber()

        # Act
        dispatcher.subscribe(subscriber)

        # Assert
        assert dispatcher.has_subscribers(HelloWorldCreated)
        assert not dispatcher.has_subscribers(HelloWorldDeleted)

    def test_subscribe_multiple_events(self):
        """Debe suscribir correctamente a múltiples eventos"""
        # Arrange
        dispatcher = EventDispatcher()
        subscriber = MockMultipleEventSubscriber()

        # Act
        dispatcher.subscribe(subscriber)

        # Assert
        assert dispatcher.has_subscribers(HelloWorldCreated)
        assert dispatcher.has_subscribers(HelloWorldDeleted)

    def test_publish_calls_subscriber_handle(self):
        """Debe llamar handle del suscriptor al publicar evento"""
        # Arrange
        dispatcher = EventDispatcher()
        subscriber = Mock(spec=MockSingleEventSubscriber)
        subscriber.subscribed_to = Mock(return_value=HelloWorldCreated)

        event = HelloWorldCreated(
            hello_world_id=1,
            greeting="Test"
        )

        # Act
        dispatcher.subscribe(subscriber)
        dispatcher.publish(event)

        # Assert
        subscriber.handle.assert_called_once_with(event)

    def test_publish_to_multiple_subscribers(self):
        """Debe notificar a todos los suscriptores del mismo evento"""
        # Arrange
        dispatcher = EventDispatcher()

        subscriber1 = Mock(spec=MockSingleEventSubscriber)
        subscriber1.subscribed_to = Mock(return_value=HelloWorldCreated)

        subscriber2 = Mock(spec=MockSingleEventSubscriber)
        subscriber2.subscribed_to = Mock(return_value=HelloWorldCreated)

        event = HelloWorldCreated(
            hello_world_id=1,
            greeting="Test"
        )

        # Act
        dispatcher.subscribe(subscriber1)
        dispatcher.subscribe(subscriber2)
        dispatcher.publish(event)

        # Assert
        subscriber1.handle.assert_called_once_with(event)
        subscriber2.handle.assert_called_once_with(event)

    def test_publish_handles_subscriber_exceptions(self):
        """Debe continuar publicando aunque un suscriptor falle"""
        # Arrange
        dispatcher = EventDispatcher()

        failing_subscriber = Mock(spec=MockSingleEventSubscriber)
        failing_subscriber.subscribed_to = Mock(return_value=HelloWorldCreated)
        failing_subscriber.handle = Mock(
            side_effect=RuntimeError("Subscriber error"))

        working_subscriber = Mock(spec=MockSingleEventSubscriber)
        working_subscriber.subscribed_to = Mock(return_value=HelloWorldCreated)

        event = HelloWorldCreated(
            hello_world_id=1,
            greeting="Test"
        )

        # Act
        dispatcher.subscribe(failing_subscriber)
        dispatcher.subscribe(working_subscriber)
        dispatcher.publish(event)

        # Assert - El working_subscriber debe ser llamado aunque failing_subscriber falle
        failing_subscriber.handle.assert_called_once()
        working_subscriber.handle.assert_called_once()

    def test_publish_multiple(self):
        """Debe publicar múltiples eventos en orden"""
        # Arrange
        dispatcher = EventDispatcher()
        subscriber = Mock(spec=MockMultipleEventSubscriber)
        subscriber.subscribed_to = Mock(
            return_value=[HelloWorldCreated, HelloWorldDeleted])

        event1 = HelloWorldCreated(
            hello_world_id=1,
            greeting="Test"
        )
        event2 = HelloWorldDeleted(
            hello_world_id=1
        )

        # Act
        dispatcher.subscribe(subscriber)
        dispatcher.publish_multiple([event1, event2])

        # Assert
        assert subscriber.handle.call_count == 2
        subscriber.handle.assert_any_call(event1)
        subscriber.handle.assert_any_call(event2)

    def test_get_subscribers(self):
        """Debe retornar lista de suscriptores para un evento"""
        # Arrange
        dispatcher = EventDispatcher()
        subscriber = MockSingleEventSubscriber()

        # Act
        dispatcher.subscribe(subscriber)
        subscribers = dispatcher.get_subscribers(HelloWorldCreated)

        # Assert
        assert len(subscribers) == 1
        assert subscriber in subscribers

    def test_clear_subscribers(self):
        """Debe limpiar todos los suscriptores"""
        # Arrange
        dispatcher = EventDispatcher()
        subscriber = MockSingleEventSubscriber()

        # Act
        dispatcher.subscribe(subscriber)
        assert dispatcher.has_subscribers(HelloWorldCreated)

        dispatcher.clear_subscribers()

        # Assert
        assert not dispatcher.has_subscribers(HelloWorldCreated)

    def test_avoid_duplicate_subscriptions(self):
        """Debe evitar suscripciones duplicadas del mismo suscriptor"""
        # Arrange
        dispatcher = EventDispatcher()
        subscriber = MockSingleEventSubscriber()

        # Act
        dispatcher.subscribe(subscriber)
        dispatcher.subscribe(subscriber)

        subscribers = dispatcher.get_subscribers(HelloWorldCreated)

        # Assert
        assert len(subscribers) == 1
