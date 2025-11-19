"""
Tests unitarios para los Use Cases de HelloWorld.
"""

import pytest
from unittest.mock import Mock, call
from Application.UseCases.HelloWorld.CreateHelloWorldUseCase import CreateHelloWorldUseCase
from Application.UseCases.HelloWorld.GetAllHelloWorldUseCase import GetAllHelloWorldUseCase
from Application.Queries.GetAllHelloWorldQuery import GetAllHelloWorldQuery
from Application.ReadModels.HelloWorldListReadModel import HelloWorldListReadModel
from Application.UseCases.HelloWorld.GetHelloWorldByIdUseCase import GetHelloWorldByIdUseCase
from Application.UseCases.HelloWorld.DeleteHelloWorldUseCase import DeleteHelloWorldUseCase
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
from Domain.HelloWorld.Exceptions.IncorrectGreetingException import IncorrectGreetingException


class TestCreateHelloWorldUseCase:
    """Tests para CreateHelloWorldUseCase."""

    def test_create_hello_world_success(self, mock_repository, mock_event_dispatcher):
        """Debería crear un HelloWorld exitosamente."""
        # Arrange
        use_case = CreateHelloWorldUseCase(
            mock_repository, mock_event_dispatcher)

        # Mock del repository.save() para retornar entidad con ID
        def save_side_effect(entity):
            entity._id = 123
            return entity
        mock_repository.save.side_effect = save_side_effect

        # Act
        result = use_case.execute("Hello World")

        # Assert
        assert result['greeting'] == "Hello World"
        mock_repository.save.assert_called_once()
        mock_event_dispatcher.publish_multiple.assert_called_once()

    def test_create_hello_world_with_invalid_greeting_raises_exception(
        self, mock_repository, mock_event_dispatcher
    ):
        """Debería lanzar excepción con greeting inválido."""
        # Arrange
        use_case = CreateHelloWorldUseCase(
            mock_repository, mock_event_dispatcher)

        # Act & Assert
        with pytest.raises(IncorrectGreetingException):
            use_case.execute("")

    def test_create_hello_world_publishes_event(self, mock_repository, mock_event_dispatcher):
        """Debería publicar evento después de crear."""
        # Arrange
        use_case = CreateHelloWorldUseCase(
            mock_repository, mock_event_dispatcher)

        def save_side_effect(entity):
            entity._id = 999
            return entity
        mock_repository.save.side_effect = save_side_effect

        # Act
        use_case.execute("Test")

        # Assert
        mock_event_dispatcher.publish_multiple.assert_called_once()
        published_events = mock_event_dispatcher.publish_multiple.call_args[0][0]
        assert len(published_events) > 0
        assert published_events[0].hello_world_id == 999


class TestGetAllHelloWorldUseCase:
    """Tests para GetAllHelloWorldUseCase."""

    def test_get_all_returns_empty_list_when_no_data(self):
        """Debería retornar lista vacía si no hay datos."""
        # Arrange
        mock_query_bus = Mock()
        # QueryBus retorna lista directa de ReadModels
        mock_query_bus.dispatch = Mock(return_value=[])

        use_case = GetAllHelloWorldUseCase(mock_query_bus)

        # Act
        result = use_case.execute()

        # Assert
        assert result == []
        mock_query_bus.dispatch.assert_called_once()

    def test_get_all_returns_list_of_hello_worlds(self):
        """Debería retornar lista de HelloWorlds."""
        # Arrange
        from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel

        mock_query_bus = Mock()
        # QueryBus retorna lista directa de ReadModels (no wrapper)
        items = [
            HelloWorldReadModel(id=1, greeting='Hello 1'),
            HelloWorldReadModel(id=2, greeting='Hello 2')
        ]
        mock_query_bus.dispatch = Mock(return_value=items)

        use_case = GetAllHelloWorldUseCase(mock_query_bus)

        # Act
        result = use_case.execute()

        # Assert
        assert len(result) == 2
        assert result[0]['greeting'] == "Hello 1"
        assert result[1]['greeting'] == "Hello 2"


class TestGetHelloWorldByIdUseCase:
    """Tests para GetHelloWorldByIdUseCase."""

    def test_get_by_id_returns_hello_world_when_exists(self, mock_repository):
        """Debería retornar HelloWorld cuando existe."""
        # Arrange
        greeting = GreetingValueObject.create("Found")
        entity = HelloWorld(greeting=greeting, id=123)

        mock_repository.find_by_id.return_value = entity
        use_case = GetHelloWorldByIdUseCase(mock_repository)

        # Act
        result = use_case.execute(123)

        # Assert
        assert result is not None
        assert result['greeting'] == "Found"
        mock_repository.find_by_id.assert_called_once_with(123)

    def test_get_by_id_returns_none_when_not_exists(self, mock_repository):
        """Debería retornar None cuando no existe."""
        # Arrange
        mock_repository.find_by_id.return_value = None
        use_case = GetHelloWorldByIdUseCase(mock_repository)

        # Act
        result = use_case.execute(999)

        # Assert
        assert result is None
        mock_repository.find_by_id.assert_called_once_with(999)


class TestDeleteHelloWorldUseCase:
    """Tests para DeleteHelloWorldUseCase."""

    def test_delete_returns_true_when_exists(
        self, mock_repository, mock_event_dispatcher
    ):
        """Debería retornar True cuando se elimina exitosamente."""
        # Arrange
        greeting = GreetingValueObject.create("To Delete")
        entity = HelloWorld(greeting=greeting, id=456)

        mock_repository.find_by_id.return_value = entity
        mock_repository.delete.return_value = True

        use_case = DeleteHelloWorldUseCase(
            mock_repository, mock_event_dispatcher)

        # Act
        result = use_case.execute(456)

        # Assert
        assert result is True
        mock_repository.delete.assert_called_once_with(456)
        mock_event_dispatcher.publish.assert_called_once()

    def test_delete_returns_false_when_not_exists(
        self, mock_repository, mock_event_dispatcher
    ):
        """Debería retornar False cuando no existe."""
        # Arrange
        mock_repository.delete.return_value = False
        use_case = DeleteHelloWorldUseCase(
            mock_repository, mock_event_dispatcher)

        # Act
        result = use_case.execute(999)

        # Assert
        assert result is False
        mock_repository.delete.assert_called_once_with(999)
        mock_event_dispatcher.publish.assert_not_called()

    def test_delete_publishes_event(self, mock_repository, mock_event_dispatcher):
        """Debería publicar evento al eliminar."""
        # Arrange
        greeting = GreetingValueObject.create("Delete Me")
        entity = HelloWorld(greeting=greeting, id=789)

        mock_repository.find_by_id.return_value = entity
        mock_repository.delete.return_value = True

        use_case = DeleteHelloWorldUseCase(
            mock_repository, mock_event_dispatcher)

        # Act
        use_case.execute(789)

        # Assert
        mock_event_dispatcher.publish.assert_called_once()
        published_event = mock_event_dispatcher.publish.call_args[0][0]
        assert published_event.hello_world_id == 789
