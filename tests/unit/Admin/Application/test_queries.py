"""
Tests unitarios para los Queries del módulo Admin.
"""

from Admin.Application.Queries.GetUserByIdQuery import GetUserByIdQuery


class TestGetUserByIdQuery:
    """Tests para GetUserByIdQuery."""

    def test_create_query_with_valid_id(self):
        """Debería crear un query con ID válido."""
        # Arrange & Act
        query = GetUserByIdQuery(id="550e8400-e29b-41d4-a716-446655440000")

        # Assert
        assert query.id == "550e8400-e29b-41d4-a716-446655440000"

    def test_query_stores_id_correctly(self):
        """El query debería almacenar el ID correctamente."""
        # Arrange
        test_id = "test-uuid-12345"

        # Act
        query = GetUserByIdQuery(id=test_id)

        # Assert
        assert query.id == test_id

    def test_query_with_different_uuid_formats(self):
        """Debería aceptar diferentes formatos de UUID."""
        # Arrange & Act
        query1 = GetUserByIdQuery(id="550e8400-e29b-41d4-a716-446655440000")
        query2 = GetUserByIdQuery(id="550e8400e29b41d4a716446655440000")

        # Assert
        assert query1.id == "550e8400-e29b-41d4-a716-446655440000"
        assert query2.id == "550e8400e29b41d4a716446655440000"
