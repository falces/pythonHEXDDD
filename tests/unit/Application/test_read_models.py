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
        assert restored.created_at.replace(microsecond=0) == original.created_at.replace(microsecond=0)


class TestHelloWorldListReadModel:
    """Tests para HelloWorldListReadModel"""
    
    def test_create_list_read_model(self):
        """Debe crear lista con metadatos de paginación"""
        # Arrange
        items = [
            HelloWorldReadModel(id=1, greeting="Test 1", created_at=datetime.now()),
            HelloWorldReadModel(id=2, greeting="Test 2", created_at=datetime.now()),
        ]
        
        # Act
        list_model = HelloWorldListReadModel(
            items=items,
            total=10,
            page=1,
            page_size=5
        )
        
        # Assert
        assert len(list_model.items) == 2
        assert list_model.total == 10
        assert list_model.page == 1
        assert list_model.page_size == 5
    
    def test_total_pages_calculation(self):
        """Debe calcular correctamente el total de páginas"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=23,
            page=1,
            page_size=10
        )
        
        # Assert
        assert list_model.total_pages == 3  # 23 items / 10 per page = 3 pages
    
    def test_total_pages_with_exact_division(self):
        """Debe calcular correctamente cuando divide exacto"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=20,
            page=1,
            page_size=10
        )
        
        # Assert
        assert list_model.total_pages == 2
    
    def test_total_pages_with_empty_results(self):
        """Debe retornar 0 páginas cuando no hay resultados"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=0,
            page=1,
            page_size=10
        )
        
        # Assert
        assert list_model.total_pages == 0
    
    def test_has_next_true(self):
        """Debe indicar que hay página siguiente"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=30,
            page=2,
            page_size=10
        )
        
        # Assert
        assert list_model.has_next is True
    
    def test_has_next_false(self):
        """Debe indicar que no hay página siguiente"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=30,
            page=3,
            page_size=10
        )
        
        # Assert
        assert list_model.has_next is False
    
    def test_has_previous_true(self):
        """Debe indicar que hay página anterior"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=30,
            page=2,
            page_size=10
        )
        
        # Assert
        assert list_model.has_previous is True
    
    def test_has_previous_false(self):
        """Debe indicar que no hay página anterior"""
        # Arrange & Act
        list_model = HelloWorldListReadModel(
            items=[],
            total=30,
            page=1,
            page_size=10
        )
        
        # Assert
        assert list_model.has_previous is False
    
    def test_to_dict(self):
        """Debe serializar lista completa a diccionario"""
        # Arrange
        items = [
            HelloWorldReadModel(id=1, greeting="Test", created_at=datetime(2024, 1, 1))
        ]
        list_model = HelloWorldListReadModel(
            items=items,
            total=1,
            page=1,
            page_size=10
        )
        
        # Act
        result = list_model.to_dict()
        
        # Assert
        assert result['total'] == 1
        assert result['page'] == 1
        assert result['page_size'] == 10
        assert result['total_pages'] == 1
        assert result['has_next'] is False
        assert result['has_previous'] is False
        assert len(result['items']) == 1
        assert result['items'][0]['id'] == 1
