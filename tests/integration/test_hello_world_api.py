"""
Tests de integración end-to-end para los endpoints de HelloWorld.
"""

import pytest
import json


@pytest.mark.integration
class TestHelloWorldEndpoints:
    """Tests E2E para los endpoints de HelloWorld."""

    def test_create_hello_world_success(self, client, db_session):
        """POST /api/v1/hello-world debería crear un nuevo HelloWorld."""
        # Arrange
        payload = {"greeting": "Test Hello World"}

        # Act
        response = client.post(
            '/api/v1/hello-world',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['status'] == 'ok'
        data = response_data['data']
        assert data['greeting'] == "Test Hello World"
        assert 'id' in data

    def test_create_hello_world_with_invalid_greeting(self, client, db_session):
        """POST /api/v1/hello-world con greeting inválido debería retornar 400."""
        # Arrange
        payload = {"greeting": ""}

        # Act
        response = client.post(
            '/api/v1/hello-world',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        assert response.status_code == 400

    def test_get_all_hello_worlds(self, client, db_session):
        """GET /api/v1/hello-world debería retornar todos los HelloWorlds."""
        # Arrange - Crear algunos HelloWorlds primero
        client.post(
            '/api/v1/hello-world',
            data=json.dumps({"greeting": "First"}),
            content_type='application/json'
        )
        client.post(
            '/api/v1/hello-world',
            data=json.dumps({"greeting": "Second"}),
            content_type='application/json'
        )

        # Act
        response = client.get('/api/v1/hello-world')

        # Assert
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['status'] == 'ok'
        data = response_data['data']
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_get_hello_world_by_id(self, client, db_session):
        """GET /api/v1/hello-world/{id} debería retornar HelloWorld específico."""
        # Arrange - Crear HelloWorld
        create_response = client.post(
            '/api/v1/hello-world',
            data=json.dumps({"greeting": "Find Me"}),
            content_type='application/json'
        )
        created_response_data = json.loads(create_response.data)
        created_data = created_response_data['data']
        created_id = created_data['id']

        # Act
        response = client.get(f'/api/v1/hello-world/{created_id}')

        # Assert
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['status'] == 'ok'
        data = response_data['data']
        assert data['greeting'] == "Find Me"
        assert data['id'] == created_id

    def test_get_hello_world_by_nonexistent_id(self, client, db_session):
        """GET /api/v1/hello-world/{id} con ID inexistente debería retornar 404."""
        # Act
        response = client.get('/api/v1/hello-world/999999')

        # Assert
        assert response.status_code == 404

    def test_delete_hello_world(self, client, db_session):
        """DELETE /api/v1/hello-world/{id} debería eliminar HelloWorld."""
        # Arrange - Crear HelloWorld
        create_response = client.post(
            '/api/v1/hello-world',
            data=json.dumps({"greeting": "Delete Me"}),
            content_type='application/json'
        )
        created_response_data = json.loads(create_response.data)
        created_data = created_response_data['data']
        created_id = created_data['id']

        # Act
        delete_response = client.delete(f'/api/v1/hello-world/{created_id}')

        # Assert
        assert delete_response.status_code == 200

        # Verificar que ya no existe
        get_response = client.get(f'/api/v1/hello-world/{created_id}')
        assert get_response.status_code == 404

    def test_delete_nonexistent_hello_world(self, client, db_session):
        """DELETE /api/v1/hello-world/{id} con ID inexistente debería retornar 404."""
        # Act
        response = client.delete('/api/v1/hello-world/888888')

        # Assert
        assert response.status_code == 404

    def test_create_multiple_hello_worlds(self, client, db_session):
        """Debería poder crear múltiples HelloWorlds."""
        # Arrange
        greetings = ["Hello 1", "Hello 2", "Hello 3", "Hello 4", "Hello 5"]

        # Act
        created_ids = []
        for greeting in greetings:
            response = client.post(
                '/api/v1/hello-world',
                data=json.dumps({"greeting": greeting}),
                content_type='application/json'
            )
            response_data = json.loads(response.data)
            data = response_data['data']
            created_ids.append(data['id'])

        # Assert
        response = client.get('/api/v1/hello-world')
        response_data = json.loads(response.data)
        all_data = response_data['data']
        assert len(all_data) >= 5

    def test_create_with_special_characters(self, client, db_session):
        """Debería manejar caracteres especiales en greeting."""
        # Arrange
        payload = {"greeting": "¡Hola Mundo! 你好世界 🌍"}

        # Act
        response = client.post(
            '/api/v1/hello-world',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['status'] == 'ok'
        data = response_data['data']
        assert data['greeting'] == "¡Hola Mundo! 你好世界 🌍"

    def test_create_with_whitespace_trimming(self, client, db_session):
        """Debería eliminar espacios en blanco al principio/final."""
        # Arrange
        payload = {"greeting": "  Trimmed Greeting  "}

        # Act
        response = client.post(
            '/api/v1/hello-world',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['status'] == 'ok'
        data = response_data['data']
        assert data['greeting'] == "Trimmed Greeting"
