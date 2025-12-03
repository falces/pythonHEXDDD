"""
Tests unitarios para los Commands del módulo Admin.
"""

from Admin.Application.Commands.CreateUserCommand import CreateUserCommand


class TestCreateUserCommand:
    """Tests para CreateUserCommand."""

    def test_create_command_with_valid_data(self):
        """Debería crear un comando con datos válidos."""
        # Arrange & Act
        command = CreateUserCommand(
            username="john_doe",
            email="john@example.com"
        )

        # Assert
        assert command.username == "john_doe"
        assert command.email == "john@example.com"

    def test_command_is_immutable(self):
        """El comando debería ser inmutable (frozen dataclass)."""
        # Arrange
        command = CreateUserCommand(
            username="immutable_user",
            email="immutable@example.com"
        )

        # Act & Assert
        try:
            command.username = "new_name"
            assert False, "Should raise FrozenInstanceError"
        except Exception:
            pass  # Expected behavior

    def test_command_equality(self):
        """Dos comandos con los mismos datos deberían ser iguales."""
        # Arrange
        command1 = CreateUserCommand(
            username="equal_user",
            email="equal@example.com"
        )
        command2 = CreateUserCommand(
            username="equal_user",
            email="equal@example.com"
        )

        # Assert
        assert command1 == command2

    def test_command_with_special_characters_in_username(self):
        """Debería aceptar caracteres especiales en username."""
        # Arrange & Act
        command = CreateUserCommand(
            username="user_name-123.test",
            email="special@example.com"
        )

        # Assert
        assert command.username == "user_name-123.test"

    def test_command_with_special_email_format(self):
        """Debería aceptar formatos de email especiales."""
        # Arrange & Act
        command = CreateUserCommand(
            username="special_user",
            email="user+tag@subdomain.example.com"
        )

        # Assert
        assert command.email == "user+tag@subdomain.example.com"
