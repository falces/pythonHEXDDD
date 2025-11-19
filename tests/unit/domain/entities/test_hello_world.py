"""
Tests unitarios para la entidad HelloWorld (Aggregate Root).
"""

import pytest
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
from Domain.HelloWorld.Events.HelloWorldCreated import HelloWorldCreated


class TestHelloWorld:
    """Tests para la entidad HelloWorld."""

    def test_create_hello_world_with_greeting(self):
        """Debería crear un HelloWorld con un greeting."""
        # Arrange
        greeting = GreetingValueObject.create("Hello World")

        # Act
        hello_world = HelloWorld.create(greeting=greeting)

        # Assert
        assert hello_world.greeting.value == "Hello World"
        assert isinstance(hello_world, HelloWorld)

    def test_create_hello_world_has_no_id_initially(self):
        """Un HelloWorld recién creado no debería tener ID."""
        # Arrange
        greeting = GreetingValueObject.create("Hello")

        # Act
        hello_world = HelloWorld.create(greeting=greeting)

        # Assert
        assert hello_world._id is None

    def test_create_hello_world_has_no_events_initially(self):
        """Un HelloWorld recién creado no debería tener eventos."""
        # Arrange
        greeting = GreetingValueObject.create("Hello")

        # Act
        hello_world = HelloWorld.create(greeting=greeting)

        # Assert
        assert hello_world.has_events is False

    def test_mark_as_created_assigns_id(self):
        """mark_as_created debería asignar el ID."""
        # Arrange
        greeting = GreetingValueObject.create("Hello")
        hello_world = HelloWorld.create(greeting=greeting)

        # Act
        hello_world.mark_as_created(id=123)

        # Assert
        assert hello_world.id == 123

    def test_mark_as_created_registers_event(self):
        """mark_as_created debería registrar un evento."""
        # Arrange
        greeting = GreetingValueObject.create("Hello")
        hello_world = HelloWorld.create(greeting=greeting)

        # Act
        hello_world.mark_as_created(id=123)

        # Assert
        assert hello_world.has_events is True

    def test_mark_as_created_event_has_correct_data(self):
        """El evento registrado debería tener los datos correctos."""
        # Arrange
        greeting = GreetingValueObject.create("Hello World")
        hello_world = HelloWorld.create(greeting=greeting)

        # Act
        hello_world.mark_as_created(id=999)
        events = hello_world.pull_domain_events()

        # Assert
        assert len(events) == 1
        assert isinstance(events[0], HelloWorldCreated)
        assert events[0].hello_world_id == 999
        assert events[0].greeting == "Hello World"

    def test_pull_domain_events_clears_events(self):
        """pull_domain_events debería limpiar los eventos."""
        # Arrange
        greeting = GreetingValueObject.create("Hello")
        hello_world = HelloWorld.create(greeting=greeting)
        hello_world.mark_as_created(id=1)

        # Act
        events = hello_world.pull_domain_events()

        # Assert
        assert len(events) == 1
        assert hello_world.has_events is False

    def test_pull_domain_events_returns_copy(self):
        """pull_domain_events debería retornar una copia."""
        # Arrange
        greeting = GreetingValueObject.create("Hello")
        hello_world = HelloWorld.create(greeting=greeting)
        hello_world.mark_as_created(id=1)

        # Act
        events1 = hello_world.pull_domain_events()
        events2 = hello_world.pull_domain_events()

        # Assert
        assert len(events1) == 1
        assert len(events2) == 0  # Ya fueron extraídos

    def test_hello_world_with_direct_constructor(self):
        """Debería poder crear HelloWorld con constructor directo."""
        # Arrange
        greeting = GreetingValueObject.create("Test")

        # Act
        hello_world = HelloWorld(greeting=greeting, id=5)

        # Assert
        assert hello_world._id == 5
        assert hello_world.greeting.value == "Test"

    def test_clear_events(self):
        """clear_events debería eliminar eventos sin retornarlos."""
        # Arrange
        greeting = GreetingValueObject.create("Hello")
        hello_world = HelloWorld.create(greeting=greeting)
        hello_world.mark_as_created(id=1)

        # Act
        hello_world.clear_events()

        # Assert
        assert hello_world.has_events is False
