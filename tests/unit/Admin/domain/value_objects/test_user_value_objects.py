"""
Tests unitarios para los Value Objects del módulo Admin.
"""

import pytest
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Admin.Domain.Exceptions.IncorrectUsernameException import IncorrectUsernameException
from Admin.Domain.Exceptions.IncorrectEmailException import IncorrectEmailException


class TestUsernameValueObject:
    """Tests para UsernameValueObject."""

    def test_create_username_with_valid_value(self):
        """Debería crear un username con un valor válido."""
        # Arrange & Act
        username = UsernameValueObject.create("john_doe")

        # Assert
        assert username.value == "john_doe"

    def test_create_username_with_minimum_length(self):
        """Debería crear un username con longitud mínima (1 caracter)."""
        # Arrange & Act
        username = UsernameValueObject.create("a")

        # Assert
        assert username.value == "a"

    def test_create_username_with_max_length(self):
        """Debería crear un username con longitud máxima (255 caracteres)."""
        # Arrange
        long_username = "a" * 255

        # Act
        username = UsernameValueObject.create(long_username)

        # Assert
        assert username.value == long_username
        assert len(username.value) == 255

    def test_create_username_with_empty_string_raises_exception(self):
        """Debería lanzar excepción con string vacío."""
        # Arrange & Act & Assert
        with pytest.raises(IncorrectUsernameException):
            UsernameValueObject.create("")

    def test_create_username_with_whitespace_only_raises_exception(self):
        """Debería lanzar excepción con solo espacios en blanco."""
        # Arrange & Act & Assert
        with pytest.raises(IncorrectUsernameException):
            UsernameValueObject.create("   ")

    def test_create_username_too_long_raises_exception(self):
        """Debería lanzar excepción con username demasiado largo."""
        # Arrange
        too_long_username = "a" * 256

        # Act & Assert
        with pytest.raises(IncorrectUsernameException):
            UsernameValueObject.create(too_long_username)

    def test_username_with_special_characters(self):
        """Debería aceptar caracteres especiales."""
        # Arrange & Act
        username = UsernameValueObject.create("user_name-123")

        # Assert
        assert username.value == "user_name-123"

    def test_username_with_unicode_characters(self):
        """Debería aceptar caracteres unicode."""
        # Arrange & Act
        username = UsernameValueObject.create("用户名")

        # Assert
        assert username.value == "用户名"


class TestEmailValueObject:
    """Tests para EmailValueObject."""

    def test_create_email_with_valid_value(self):
        """Debería crear un email con un valor válido."""
        # Arrange & Act
        email = EmailValueObject.create("john@example.com")

        # Assert
        assert email.value == "john@example.com"

    def test_create_email_with_minimum_length(self):
        """Debería crear un email con longitud mínima (1 caracter)."""
        # Arrange & Act
        email = EmailValueObject.create("a")

        # Assert
        assert email.value == "a"

    def test_create_email_with_max_length(self):
        """Debería crear un email con longitud máxima (255 caracteres)."""
        # Arrange
        long_email = "a" * 255

        # Act
        email = EmailValueObject.create(long_email)

        # Assert
        assert email.value == long_email
        assert len(email.value) == 255

    def test_create_email_with_empty_string_raises_exception(self):
        """Debería lanzar excepción con string vacío."""
        # Arrange & Act & Assert
        with pytest.raises(IncorrectEmailException):
            EmailValueObject.create("")

    def test_create_email_with_whitespace_only_raises_exception(self):
        """Debería lanzar excepción con solo espacios en blanco."""
        # Arrange & Act & Assert
        with pytest.raises(IncorrectEmailException):
            EmailValueObject.create("   ")

    def test_create_email_too_long_raises_exception(self):
        """Debería lanzar excepción con email demasiado largo."""
        # Arrange
        too_long_email = "a" * 256

        # Act & Assert
        with pytest.raises(IncorrectEmailException):
            EmailValueObject.create(too_long_email)

    def test_email_with_subdomain(self):
        """Debería aceptar emails con subdominios."""
        # Arrange & Act
        email = EmailValueObject.create("user@mail.example.com")

        # Assert
        assert email.value == "user@mail.example.com"

    def test_email_with_plus_sign(self):
        """Debería aceptar emails con signo +."""
        # Arrange & Act
        email = EmailValueObject.create("user+tag@example.com")

        # Assert
        assert email.value == "user+tag@example.com"
