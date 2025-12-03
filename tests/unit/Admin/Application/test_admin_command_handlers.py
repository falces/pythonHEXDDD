"""
Tests unitarios para los Command Handlers del módulo Admin.
"""

from unittest.mock import Mock, patch
from Admin.Application.CommandHandlers.CreateUserHander import CreateUserHander
from Admin.Application.Commands.CreateUserCommand import CreateUserCommand
from Admin.Domain.User import User
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class TestCreateUserHandler:
    """Tests para CreateUserHandler."""

    def test_handle_creates_user_and_saves(self):
        """Debería crear un usuario y guardarlo."""
        # Arrange
        mock_repository = Mock()
        mock_event_dispatcher = Mock()
        
        username = UsernameValueObject.create("test_user")
        email = EmailValueObject.create("test@example.com")
        test_id = UuidValueObject.create("550e8400-e29b-41d4-a716-446655440000")
        
        saved_user = User.create(username=username, email=email, id=test_id)
        mock_repository.save.return_value = saved_user
        
        handler = CreateUserHander(
            write_repository=mock_repository,
            event_dispatcher=mock_event_dispatcher
        )
        
        command = CreateUserCommand(
            username="test_user",
            email="test@example.com"
        )

        # Act
        result = handler.handle(command)

        # Assert
        mock_repository.save.assert_called_once()
        assert result is not None

    def test_handle_publishes_domain_events(self):
        """Debería publicar los eventos de dominio."""
        # Arrange
        mock_repository = Mock()
        mock_event_dispatcher = Mock()
        
        username = UsernameValueObject.create("event_user")
        email = EmailValueObject.create("event@example.com")
        test_id = UuidValueObject.create("550e8400-e29b-41d4-a716-446655440001")
        
        saved_user = User.create(username=username, email=email, id=test_id)
        mock_repository.save.return_value = saved_user
        
        handler = CreateUserHander(
            write_repository=mock_repository,
            event_dispatcher=mock_event_dispatcher
        )
        
        command = CreateUserCommand(
            username="event_user",
            email="event@example.com"
        )

        # Act
        handler.handle(command)

        # Assert
        mock_event_dispatcher.publish_multiple.assert_called_once()

    def test_handle_returns_user_id(self):
        """Debería devolver el ID del usuario creado como string."""
        # Arrange
        mock_repository = Mock()
        mock_event_dispatcher = Mock()
        
        username = UsernameValueObject.create("id_user")
        email = EmailValueObject.create("id@example.com")
        expected_id = UuidValueObject.create("550e8400-e29b-41d4-a716-446655440002")
        
        saved_user = User.create(username=username, email=email, id=expected_id)
        mock_repository.save.return_value = saved_user
        
        handler = CreateUserHander(
            write_repository=mock_repository,
            event_dispatcher=mock_event_dispatcher
        )
        
        command = CreateUserCommand(
            username="id_user",
            email="id@example.com"
        )

        # Act
        result = handler.handle(command)

        # Assert
        assert result == "550e8400-e29b-41d4-a716-446655440002"

    def test_handle_creates_user_with_correct_data(self):
        """Debería crear el usuario con los datos correctos del comando."""
        # Arrange
        mock_repository = Mock()
        mock_event_dispatcher = Mock()
        
        username = UsernameValueObject.create("correct_user")
        email = EmailValueObject.create("correct@example.com")
        test_id = UuidValueObject.create("550e8400-e29b-41d4-a716-446655440003")
        
        saved_user = User.create(username=username, email=email, id=test_id)
        mock_repository.save.return_value = saved_user
        
        handler = CreateUserHander(
            write_repository=mock_repository,
            event_dispatcher=mock_event_dispatcher
        )
        
        command = CreateUserCommand(
            username="correct_user",
            email="correct@example.com"
        )

        # Act
        handler.handle(command)

        # Assert
        saved_user_arg = mock_repository.save.call_args[0][0]
        assert saved_user_arg.username.value == "correct_user"
        assert saved_user_arg.email.value == "correct@example.com"
