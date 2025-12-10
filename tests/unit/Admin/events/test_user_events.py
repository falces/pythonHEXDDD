"""
Tests unitarios para los Domain Events del módulo Admin.
"""

from Admin.Domain.Events.UserCreated import UserCreated


class TestUserCreatedEvent:
    """Tests para el evento UserCreated."""

    def test_create_event_with_valid_data(self):
        """Debería crear un evento con datos válidos."""
        # Arrange & Act
        event = UserCreated(
            user_id="550e8400-e29b-41d4-a716-446655440000",
            username="john_doe",
            email="john@example.com"
        )

        # Assert
        assert event.id == "550e8400-e29b-41d4-a716-446655440000"
        assert event.username == "john_doe"
        assert event.email == "john@example.com"

    def test_event_has_occurred_on_timestamp(self):
        """El evento debería tener un timestamp de occurred_on."""
        # Arrange & Act
        event = UserCreated(
            user_id="test-id",
            username="test_user",
            email="test@example.com"
        )

        # Assert
        assert event.occurred_on is not None

    def test_event_has_unique_event_id(self):
        """Cada evento debería tener un ID único."""
        # Arrange & Act
        event1 = UserCreated(
            user_id="id-1",
            username="user1",
            email="user1@example.com"
        )
        event2 = UserCreated(
            user_id="id-2",
            username="user2",
            email="user2@example.com"
        )

        # Assert
        assert event1.event_id != event2.event_id

    def test_event_to_dict_contains_all_data(self):
        """to_dict debería contener todos los datos del evento."""
        # Arrange
        event = UserCreated(
            user_id="dict-test-id",
            username="dict_user",
            email="dict@example.com"
        )

        # Act
        result = event.to_dict()

        # Assert
        assert result["id"] == "dict-test-id"
        assert result["username"] == "dict_user"
        assert result["email"] == "dict@example.com"
        assert "event_id" in result
        assert "occurred_on" in result

    def test_event_repr(self):
        """__repr__ debería devolver una representación legible."""
        # Arrange
        event = UserCreated(
            user_id="repr-id",
            username="repr_user",
            email="repr@example.com"
        )

        # Act
        result = repr(event)

        # Assert
        assert "UserCreated" in result
        assert "repr-id" in result
        assert "repr_user" in result
        assert "repr@example.com" in result
