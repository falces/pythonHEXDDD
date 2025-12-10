"""
Tests unitarios para los Read Models del módulo Admin.
"""

from Admin.Application.ReadModels.UserReadModel import UserReadModel


class TestUserReadModel:
    """Tests para UserReadModel."""

    def test_create_read_model(self):
        """Debería crear un read model con todos los campos."""
        # Arrange & Act
        read_model = UserReadModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            username="test_user",
            email="test@example.com"
        )

        # Assert
        assert read_model.id == "550e8400-e29b-41d4-a716-446655440000"
        assert read_model.username == "test_user"
        assert read_model.email == "test@example.com"

    def test_to_dict(self):
        """to_dict debería devolver un diccionario con todos los datos."""
        # Arrange
        read_model = UserReadModel(
            id="dict-uuid",
            username="dict_user",
            email="dict@example.com"
        )

        # Act
        result = read_model.to_dict()

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == "dict-uuid"
        assert result["username"] == "dict_user"
        assert result["email"] == "dict@example.com"

    def test_from_dict(self):
        """from_dict debería crear un read model desde un diccionario."""
        # Arrange
        data = {
            "id": "from-dict-uuid",
            "username": "from_dict_user",
            "email": "from_dict@example.com"
        }

        # Act
        read_model = UserReadModel.from_dict(data)

        # Assert
        assert read_model.id == "from-dict-uuid"
        assert read_model.username == "from_dict_user"
        assert read_model.email == "from_dict@example.com"

    def test_round_trip_serialization(self):
        """Debería mantener los datos tras to_dict y from_dict."""
        # Arrange
        original = UserReadModel(
            id="round-trip-uuid",
            username="round_trip_user",
            email="round_trip@example.com"
        )

        # Act
        dict_data = original.to_dict()
        restored = UserReadModel.from_dict(dict_data)

        # Assert
        assert restored.id == original.id
        assert restored.username == original.username
        assert restored.email == original.email

    def test_to_dict_returns_new_dict(self):
        """to_dict debería devolver un nuevo diccionario cada vez."""
        # Arrange
        read_model = UserReadModel(
            id="new-dict-uuid",
            username="new_dict_user",
            email="new_dict@example.com"
        )

        # Act
        dict1 = read_model.to_dict()
        dict2 = read_model.to_dict()

        # Assert
        assert dict1 == dict2
        assert dict1 is not dict2
