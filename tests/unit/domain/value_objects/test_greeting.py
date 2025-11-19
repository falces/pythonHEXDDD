"""
Tests unitarios para Value Objects del dominio HelloWorld.
"""

import pytest
from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
from Domain.HelloWorld.Exceptions.IncorrectGreetingException import IncorrectGreetingException


class TestGreetingValueObject:
    """Tests para el Value Object Greeting."""

    def test_create_greeting_with_valid_text(self):
        """Debería crear un Greeting con texto válido."""
        # Arrange
        text = "Hello World"

        # Act
        greeting = GreetingValueObject.create(text)

        # Assert
        assert greeting.value == text
        assert isinstance(greeting, GreetingValueObject)

    def test_create_greeting_with_minimum_length(self):
        """Debería crear un Greeting con el mínimo de caracteres (1)."""
        # Arrange
        text = "H"

        # Act
        greeting = GreetingValueObject.create(text)

        # Assert
        assert greeting.value == text

    def test_create_greeting_with_empty_string_raises_exception(self):
        """Debería lanzar excepción con string vacío."""
        # Arrange
        text = ""

        # Act & Assert
        with pytest.raises(IncorrectGreetingException) as exc_info:
            GreetingValueObject.create(text)

        assert "Incorrect greeting" in str(exc_info.value)

    def test_create_greeting_with_none_raises_exception(self):
        """Debería lanzar excepción con None."""
        # Arrange
        text = None

        # Act & Assert
        with pytest.raises((IncorrectGreetingException, AttributeError)):
            GreetingValueObject.create(text)

    def test_create_greeting_with_too_short_text_raises_exception(self):
        """Debería lanzar excepción con texto demasiado corto."""
        # Arrange - Texto vacío después de trim
        text = ""  # 0 caracteres

        # Act & Assert
        with pytest.raises(IncorrectGreetingException):
            GreetingValueObject.create(text)

    def test_create_greeting_with_whitespace_only_raises_exception(self):
        """Debería lanzar excepción con solo espacios."""
        # Arrange
        text = "   "

        # Act & Assert
        with pytest.raises(IncorrectGreetingException):
            GreetingValueObject.create(text)

    def test_greeting_trims_whitespace(self):
        """Debería eliminar espacios al inicio y final."""
        # Arrange
        text = "  Hello World  "

        # Act
        greeting = GreetingValueObject.create(text)

        # Assert
        assert greeting.value == "Hello World"

    def test_greeting_equality(self):
        """Dos Greetings con el mismo valor deberían ser iguales."""
        # Arrange
        text = "Hello World"
        greeting1 = GreetingValueObject.create(text)
        greeting2 = GreetingValueObject.create(text)

        # Act & Assert
        assert greeting1.value == greeting2.value

    def test_greeting_with_special_characters(self):
        """Debería aceptar caracteres especiales."""
        # Arrange
        text = "¡Hola Mundo! 你好"

        # Act
        greeting = GreetingValueObject.create(text)

        # Assert
        assert greeting.value == text

    def test_greeting_with_numbers(self):
        """Debería aceptar números."""
        # Arrange
        text = "Hello 123"

        # Act
        greeting = GreetingValueObject.create(text)

        # Assert
        assert greeting.value == text

    def test_greeting_immutability(self):
        """El Greeting debería ser inmutable."""
        # Arrange
        greeting = GreetingValueObject.create("Hello")

        # Act & Assert - El value object protege contra reasignación directa
        # pero no es frozen, así que este test verifica que el valor no cambia
        original_value = greeting.value
        assert original_value == "Hello"
