"""
Tests unitarios para Read Models (CQRS).
Valida serialización y cálculos de paginación.
"""

import pytest
from datetime import datetime
from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel
from Application.ReadModels.HelloWorldListReadModel import HelloWorldListReadModel


class TestHelloWorldReadModel:
    """Tests para HelloWorldReadModel"""

    def test_create_read_model(self):
        """Debe crear read model con todos los campos"""
        # Arrange & Act
        now = datetime.now()
        read_model = HelloWorldReadModel(
            id=1,
            greeting="Test Greeting",
            created_at=now
        )

        # Assert
        assert read_model.id == 1
        assert read_model.greeting == "Test Greeting"
        assert read_model.created_at == now

    def test_to_dict(self):
        """Debe serializar a diccionario correctamente"""
        # Arrange
        now = datetime(2024, 1, 1, 12, 0, 0)
        read_model = HelloWorldReadModel(
            id=1,
            greeting="Test",
            created_at=now
        )

        # Act
        result = read_model.to_dict()

        # Assert
        assert result == {
            'id': 1,
            'greeting': 'Test',
            'created_at': '2024-01-01T12:00:00'
        }

    def test_from_dict(self):
        """Debe deserializar desde diccionario correctamente"""
        # Arrange
        data = {
            'id': 1,
            'greeting': 'Test',
            'created_at': '2024-01-01T12:00:00'
        }

        # Act
        read_model = HelloWorldReadModel.from_dict(data)

        # Assert
        assert read_model.id == 1
        assert read_model.greeting == 'Test'
        assert read_model.created_at == datetime(2024, 1, 1, 12, 0, 0)

    def test_round_trip_serialization(self):
        """Debe mantener datos intactos en serialización ida y vuelta"""
        # Arrange
        original = HelloWorldReadModel(
            id=42,
            greeting="Round trip test",
            created_at=datetime.now()
        )

        # Act
        data = original.to_dict()
        restored = HelloWorldReadModel.from_dict(data)

        # Assert
        assert restored.id == original.id
        assert restored.greeting == original.greeting
        # Comparar fechas sin microsegundos (el isoformat puede perder precisión)
        assert restored.created_at.replace(
            microsecond=0) == original.created_at.replace(microsecond=0)


class TestHelloWorldListReadModel:
    """Tests para HelloWorldListReadModel"""

    def test_create_list_read_model(self):
        """Debe crear lista con metadatos de paginación"""
        # Arrange
        items = [
            HelloWorldReadModel(id=1, greeting="Test 1",
                                created_at=datetime.now()),
            HelloWorldReadModel(id=2, greeting="Test 2",
                                created_at=datetime.now()),
        ]

        # Act
        list_model = HelloWorldListReadModel(
            items=items,
            total=10,
            limit=5,
            offset=0
        )

        # Assert
        assert len(list_model.items) == 2
        assert list_model.total == 10
        assert list_model.limit == 5
        assert list_model.offset == 0

    def test_has_next_property(self):
        """Debe calcular correctamente has_next"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=23,
            limit=10,
            offset=0
        )

        # Assert
        assert list_model.has_next is True

    def test_has_next_last_page(self):
        """Debe retornar False en última página"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=20,
            limit=10,
            offset=10
        )

        # Assert
        assert list_model.has_next is False

    def test_has_previous_with_offset(self):
        """Debe retornar True cuando hay offset > 0"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=30,
            limit=10,
            offset=10
        )

        # Assert
        assert list_model.has_previous is True

    def test_has_next_true(self):
        """Debe indicar que hay página siguiente"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=30,
            limit=10,
            offset=10
        )

        # Assert
        assert list_model.has_next is True

    def test_has_next_false(self):
        """Debe indicar que no hay página siguiente"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=30,
            limit=10,
            offset=20
        )

        # Assert
        assert list_model.has_next is False

    def test_has_previous_true(self):
        """Debe indicar que hay página anterior"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=30,
            limit=10,
            offset=10
        )

        # Assert
        assert list_model.has_previous is True

    def test_has_previous_false(self):
        """Debe indicar que no hay página anterior"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=30,
            limit=10,
            offset=0
        )

        # Assert
        assert list_model.has_previous is False

    def test_to_dict(self):
        """Debe serializar lista completa a diccionario"""
        # Arrange
        items = [
            HelloWorldReadModel(id=1, greeting="Test",
                                created_at=datetime(2024, 1, 1))
        ]
        list_model = HelloWorldListReadModel(
            items=items,
            total=1,
            limit=10,
            offset=0
        )

        # Act
        result = list_model.to_dict()

        # Assert
        assert result['total'] == 1
        assert result['limit'] == 10
        assert result['offset'] == 0
        assert result['has_next'] is False
        assert result['has_previous'] is False
        assert len(result['items']) == 1
        assert result['items'][0]['id'] == 1
