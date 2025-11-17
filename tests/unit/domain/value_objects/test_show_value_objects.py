"""
Tests unitarios para Value Objects del dominio Show.
"""

import pytest
from Domain.Show.ValueObjects.ShowId import ShowId
from Domain.Show.ValueObjects.ShowTitle import ShowTitle
from Domain.Show.ValueObjects.ShowType import ShowType
from Domain.Show.ValueObjects.StreamingOption import StreamingOption
from Shared.Domain.Exceptions.IncorrectValueException import IncorrectValueException


class TestShowId:
    """Tests para el Value Object ShowId."""
    
    def test_create_show_id_with_valid_value(self):
        """Debería crear un ShowId con valor válido."""
        # Arrange
        value = "tt1234567"
        
        # Act
        show_id = ShowId(value)
        
        # Assert
        assert show_id.value == value
    
    def test_create_show_id_with_empty_string_raises_exception(self):
        """Debería lanzar excepción con string vacío."""
        # Arrange
        value = ""
        
        # Act & Assert
        with pytest.raises(IncorrectValueException):
            ShowId(value)
    
    def test_show_id_equality(self):
        """Dos ShowIds con el mismo valor deberían ser iguales."""
        # Arrange
        value = "tt1234567"
        show_id1 = ShowId(value)
        show_id2 = ShowId(value)
        
        # Act & Assert
        assert show_id1.value == show_id2.value


class TestShowTitle:
    """Tests para el Value Object ShowTitle."""
    
    def test_create_show_title_with_valid_text(self):
        """Debería crear un ShowTitle con texto válido."""
        # Arrange
        text = "Breaking Bad"
        
        # Act
        title = ShowTitle(text)
        
        # Assert
        assert title.value == text
    
    def test_create_show_title_with_empty_string_raises_exception(self):
        """Debería lanzar excepción con string vacío."""
        # Arrange
        text = ""
        
        # Act & Assert
        with pytest.raises(IncorrectValueException):
            ShowTitle(text)
    
    def test_show_title_with_special_characters(self):
        """Debería aceptar caracteres especiales."""
        # Arrange
        text = "Game of Thrones: Season 1"
        
        # Act
        title = ShowTitle(text)
        
        # Assert
        assert title.value == text


class TestShowType:
    """Tests para el Value Object ShowType."""
    
    def test_create_show_type_movie(self):
        """Debería crear un ShowType de tipo movie."""
        # Arrange
        value = "movie"
        
        # Act
        show_type = ShowType(value)
        
        # Assert
        assert show_type.value == value
        assert show_type.is_movie()
        assert not show_type.is_series()
    
    def test_create_show_type_series(self):
        """Debería crear un ShowType de tipo series."""
        # Arrange
        value = "series"
        
        # Act
        show_type = ShowType(value)
        
        # Assert
        assert show_type.value == value
        assert show_type.is_series()
        assert not show_type.is_movie()
    
    def test_create_show_type_with_invalid_value_raises_exception(self):
        """Debería lanzar excepción con valor inválido."""
        # Arrange
        value = "invalid"
        
        # Act & Assert
        with pytest.raises(IncorrectValueException) as exc_info:
            ShowType(value)
        
        assert "movie or series" in str(exc_info.value).lower()


class TestStreamingOption:
    """Tests para el Value Object StreamingOption."""
    
    def test_create_streaming_option_with_valid_data(self):
        """Debería crear un StreamingOption con datos válidos."""
        # Arrange
        service = "Netflix"
        streaming_type = "subscription"
        
        # Act
        option = StreamingOption(service, streaming_type)
        
        # Assert
        assert option.service == service
        assert option.streaming_type == streaming_type
    
    def test_create_streaming_option_with_empty_service_raises_exception(self):
        """Debería lanzar excepción con servicio vacío."""
        # Arrange
        service = ""
        streaming_type = "subscription"
        
        # Act & Assert
        with pytest.raises(IncorrectValueException):
            StreamingOption(service, streaming_type)
    
    def test_create_streaming_option_with_empty_type_raises_exception(self):
        """Debería lanzar excepción con tipo vacío."""
        # Arrange
        service = "Netflix"
        streaming_type = ""
        
        # Act & Assert
        with pytest.raises(IncorrectValueException):
            StreamingOption(service, streaming_type)
    
    def test_streaming_option_to_dict(self):
        """Debería serializar correctamente a diccionario."""
        # Arrange
        service = "Netflix"
        streaming_type = "subscription"
        option = StreamingOption(service, streaming_type)
        
        # Act
        result = option.to_dict()
        
        # Assert
        assert result == {
            "service": service,
            "type": streaming_type
        }
