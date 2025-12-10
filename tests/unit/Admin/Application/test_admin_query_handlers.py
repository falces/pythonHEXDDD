"""
Tests unitarios para los Query Handlers del módulo Admin.
"""

from unittest.mock import Mock
from Admin.Application.QueryHandlers.GetUserByIdHandler import GetUserByIdHandler
from Admin.Application.Queries.GetUserByIdQuery import GetUserByIdQuery
from Admin.Application.ReadModels.UserReadModel import UserReadModel


class TestGetUserByIdHandler:
    """Tests para GetUserByIdHandler."""

    def test_handle_returns_user_when_found(self):
        """Debería devolver el usuario cuando existe."""
        # Arrange
        mock_repository = Mock()
        
        user_read_model = UserReadModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            username="found_user",
            email="found@example.com"
        )
        mock_repository.find_by_id.return_value = user_read_model
        
        handler = GetUserByIdHandler(read_repository=mock_repository)
        query = GetUserByIdQuery(id="550e8400-e29b-41d4-a716-446655440000")

        # Act
        result = handler.handle(query)

        # Assert
        assert result is not None
        assert result["id"] == "550e8400-e29b-41d4-a716-446655440000"
        assert result["username"] == "found_user"
        assert result["email"] == "found@example.com"

    def test_handle_calls_repository_with_correct_id(self):
        """Debería llamar al repositorio con el ID correcto."""
        # Arrange
        mock_repository = Mock()
        user_read_model = UserReadModel(
            id="test-uuid-12345",
            username="test_user",
            email="test@example.com"
        )
        mock_repository.find_by_id.return_value = user_read_model
        
        handler = GetUserByIdHandler(read_repository=mock_repository)
        query = GetUserByIdQuery(id="test-uuid-12345")

        # Act
        handler.handle(query)

        # Assert
        mock_repository.find_by_id.assert_called_once_with("test-uuid-12345")

    def test_handle_returns_dict_format(self):
        """Debería devolver el resultado en formato diccionario."""
        # Arrange
        mock_repository = Mock()
        
        user_read_model = UserReadModel(
            id="dict-uuid",
            username="dict_user",
            email="dict@example.com"
        )
        mock_repository.find_by_id.return_value = user_read_model
        
        handler = GetUserByIdHandler(read_repository=mock_repository)
        query = GetUserByIdQuery(id="dict-uuid")

        # Act
        result = handler.handle(query)

        # Assert
        assert isinstance(result, dict)
        assert "id" in result
        assert "username" in result
        assert "email" in result
