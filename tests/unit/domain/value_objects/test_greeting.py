"""
Tests unitarios para Value Objects del dominio HelloWorld.
"""

import pytest
from Domain.HelloWorld.ValueObjects.Greeting import Greeting
from Domain.HelloWorld.Exceptions.IncorrectGreetingException import IncorrectGreetingException


class TestGreeting:
    """Tests para el Value Object Greeting."""
    
    def test_create_greeting_with_valid_text(self):
        """Debería crear un Greeting con texto válido."""
        # Arrange
        text = "Hello World"
        
        # Act
        greeting = Greeting.create(text)
        
        # Assert
        assert greeting.value == text
        assert isinstance(greeting, Greeting)
    
    def test_create_greeting_with_minimum_length(self):
        """Debería crear un Greeting con el mínimo de caracteres (3)."""
        # Arrange
        text = "Hi!"
        
        # Act
        greeting = Greeting.create(text)
        
        # Assert
        assert greeting.value == text
    
    def test_create_greeting_with_empty_string_raises_exception(self):
        """Debería lanzar excepción con string vacío."""
        # Arrange
        text = ""
        
        # Act & Assert
        with pytest.raises(IncorrectGreetingException) as exc_info:
            Greeting.create(text)
        
        assert "Greeting cannot be empty" in str(exc_info.value)
    
    def test_create_greeting_with_none_raises_exception(self):
        """Debería lanzar excepción con None."""
        # Arrange
        text = None
        
        # Act & Assert
        with pytest.raises(IncorrectGreetingException):
            Greeting.create(text)
    
    def test_create_greeting_with_too_short_text_raises_exception(self):
        """Debería lanzar excepción con texto demasiado corto."""
        # Arrange
        text = "Hi"  # Solo 2 caracteres
        
        # Act & Assert
        with pytest.raises(IncorrectGreetingException) as exc_info:
            Greeting.create(text)
        
        assert "too short" in str(exc_info.value).lower() or "minimum" in str(exc_info.value).lower()
    
    def test_create_greeting_with_whitespace_only_raises_exception(self):
        """Debería lanzar excepción con solo espacios."""
        # Arrange
        text = "   "
        
        # Act & Assert
        with pytest.raises(IncorrectGreetingException):
            Greeting.create(text)
    
    def test_greeting_trims_whitespace(self):
        """Debería eliminar espacios al inicio y final."""
        # Arrange
        text = "  Hello World  "
        
        # Act
        greeting = Greeting.create(text)
        
        # Assert
        assert greeting.value == "Hello World"
    
    def test_greeting_equality(self):
        """Dos Greetings con el mismo valor deberían ser iguales."""
        # Arrange
        text = "Hello World"
        greeting1 = Greeting.create(text)
        greeting2 = Greeting.create(text)
        
        # Act & Assert
        assert greeting1.value == greeting2.value
    
    def test_greeting_with_special_characters(self):
        """Debería aceptar caracteres especiales."""
        # Arrange
        text = "¡Hola Mundo! 你好"
        
        # Act
        greeting = Greeting.create(text)
        
        # Assert
        assert greeting.value == text
    
    def test_greeting_with_numbers(self):
        """Debería aceptar números."""
        # Arrange
        text = "Hello 123"
        
        # Act
        greeting = Greeting.create(text)
        
        # Assert
        assert greeting.value == text
    
    def test_greeting_immutability(self):
        """El Greeting debería ser inmutable."""
        # Arrange
        greeting = Greeting.create("Hello")
        
        # Act & Assert
        with pytest.raises(AttributeError):
            greeting.value = "New Value"
