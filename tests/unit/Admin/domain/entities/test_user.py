"""
Tests unitarios para la entidad User (Aggregate Root).
"""

from Admin.Domain.User import User
from Admin.Domain.ValueObjects.UsernameValueObject import UsernameValueObject
from Admin.Domain.ValueObjects.EmailValueObject import EmailValueObject
from Admin.Domain.Events.UserCreated import UserCreated
from Shared.Domain.ValueObjects.UuidValueObject import UuidValueObject


class TestUser:
    """Tests para la entidad User."""

    def test_create_user_with_username_and_email(self):
        """Debería crear un User con username y email."""
        # Arrange
        username = UsernameValueObject.create("john_doe")
        email = EmailValueObject.create("john@example.com")

        # Act
        user = User.create(username=username, email=email)

        # Assert
        assert user.username.value == "john_doe"
        assert user.email.value == "john@example.com"
        assert isinstance(user, User)

    def test_create_user_generates_uuid_automatically(self):
        """Un User recién creado debería tener un UUID generado automáticamente."""
        # Arrange
        username = UsernameValueObject.create("jane_doe")
        email = EmailValueObject.create("jane@example.com")

        # Act
        user = User.create(username=username, email=email)

        # Assert
        assert user.id is not None
        assert isinstance(user.id, UuidValueObject)
        assert len(user.id.value) == 36  # UUID format

    def test_create_user_with_custom_id(self):
        """Debería crear un User con un ID personalizado."""
        # Arrange
        username = UsernameValueObject.create("custom_user")
        email = EmailValueObject.create("custom@example.com")
        custom_id = UuidValueObject.create("550e8400-e29b-41d4-a716-446655440000")

        # Act
        user = User.create(username=username, email=email, id=custom_id)

        # Assert
        assert user.id.value == "550e8400-e29b-41d4-a716-446655440000"

    def test_create_user_has_no_events_initially(self):
        """Un User recién creado no debería tener eventos."""
        # Arrange
        username = UsernameValueObject.create("test_user")
        email = EmailValueObject.create("test@example.com")

        # Act
        user = User.create(username=username, email=email)

        # Assert
        assert user.has_events is False

    def test_mark_as_created_records_user_created_event(self):
        """mark_as_created debería registrar un evento UserCreated."""
        # Arrange
        username = UsernameValueObject.create("event_user")
        email = EmailValueObject.create("event@example.com")
        user = User.create(username=username, email=email)

        # Act
        user.mark_as_created()

        # Assert
        assert user.has_events is True
        events = user.pull_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], UserCreated)

    def test_mark_as_created_contains_correct_data(self):
        """El evento UserCreated debería contener los datos correctos."""
        # Arrange
        username = UsernameValueObject.create("data_user")
        email = EmailValueObject.create("data@example.com")
        user = User.create(username=username, email=email)

        # Act
        user.mark_as_created()

        # Assert
        events = user.pull_domain_events()
        event = events[0]
        assert event.username == "data_user"
        assert event.email == "data@example.com"

    def test_pull_domain_events_clears_events(self):
        """pull_domain_events debería limpiar los eventos."""
        # Arrange
        username = UsernameValueObject.create("clear_user")
        email = EmailValueObject.create("clear@example.com")
        user = User.create(username=username, email=email)
        user.mark_as_created()

        # Act
        user.pull_domain_events()

        # Assert
        assert user.has_events is False

    def test_two_users_have_different_ids(self):
        """Dos usuarios creados por separado deben tener IDs diferentes."""
        # Arrange
        username1 = UsernameValueObject.create("user1")
        email1 = EmailValueObject.create("user1@example.com")
        username2 = UsernameValueObject.create("user2")
        email2 = EmailValueObject.create("user2@example.com")

        # Act
        user1 = User.create(username=username1, email=email1)
        user2 = User.create(username=username2, email=email2)

        # Assert
        assert user1.id.value != user2.id.value
