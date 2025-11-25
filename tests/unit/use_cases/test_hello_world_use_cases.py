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
from Application.Commands.CreateHelloWorldCommand import CreateHelloWorldCommand
from Application.Commands.DeleteHelloWorldCommand import DeleteHelloWorldCommand
from Domain.HelloWorld.HelloWorld import HelloWorld
from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
from Domain.HelloWorld.Exceptions.IncorrectGreetingException import IncorrectGreetingException
from Application.UseCases.HelloWorld.DeleteHelloWorldUseCase import DeleteHelloWorldUseCase


class TestCreateHelloWorldUseCase:
    """Tests para CreateHelloWorldUseCase (Refactorizado CQRS)."""

    def test_create_hello_world_success(self):
        """Debería crear un comando y despacharlo al bus."""
        # Arrange
        mock_command_bus = Mock()
        mock_command_bus.dispatch.return_value = 123  # ID retornado por el handler

        use_case = CreateHelloWorldUseCase(mock_command_bus)

        # Act
        result = use_case.execute("Hello World")

        # Assert
        # Verifica que se retorna el formato esperado por el controlador
        assert result == {"id": 123, "greeting": "Hello World"}

        # Verifica que se despachó el comando correcto
        mock_command_bus.dispatch.assert_called_once()
        args = mock_command_bus.dispatch.call_args[0]
        command = args[0]
        assert isinstance(command, CreateHelloWorldCommand)
        assert command.greeting_text == "Hello World"

    def test_create_propagates_exceptions(self):
        """Debería propagar excepciones lanzadas por el handler."""
        # Arrange
        mock_command_bus = Mock()
        mock_command_bus.dispatch.side_effect = IncorrectGreetingException(
            "Invalid")

        use_case = CreateHelloWorldUseCase(mock_command_bus)

        # Act & Assert
        with pytest.raises(IncorrectGreetingException):
            use_case.execute("")


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

    def test_get_by_id_returns_hello_world_when_exists(self):
        """Debería retornar HelloWorld cuando existe."""
        # Arrange
        from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel
        from Application.Queries.GetHelloWorldByIdQuery import GetHelloWorldByIdQuery

        mock_query_bus = Mock()
        read_model = HelloWorldReadModel(id=123, greeting="Found")
        mock_query_bus.dispatch.return_value = read_model

        use_case = GetHelloWorldByIdUseCase(mock_query_bus)

        # Act
        result = use_case.execute(123)

        # Assert
        assert result is not None
        assert result['greeting'] == "Found"
        mock_query_bus.dispatch.assert_called_once_with(
            GetHelloWorldByIdQuery(id=123))

    def test_get_by_id_returns_none_when_not_exists(self):
        """Debería retornar None cuando no existe."""
        # Arrange
        from Application.Queries.GetHelloWorldByIdQuery import GetHelloWorldByIdQuery

        mock_query_bus = Mock()
        mock_query_bus.dispatch.return_value = None

        use_case = GetHelloWorldByIdUseCase(mock_query_bus)

        # Act
        result = use_case.execute(999)

        # Assert
        assert result is None
        mock_query_bus.dispatch.assert_called_once_with(
            GetHelloWorldByIdQuery(id=999))


class TestDeleteHelloWorldUseCase:
    """Tests para DeleteHelloWorldUseCase (Refactorizado CQRS)."""

    def test_delete_returns_true_when_exists(self):
        """Debería retornar True cuando el bus confirma eliminación."""
        # Arrange
        mock_command_bus = Mock()
        mock_command_bus.dispatch.return_value = True

        use_case = DeleteHelloWorldUseCase(mock_command_bus)

        # Act
        result = use_case.execute(456)

        # Assert
        assert result is True
        mock_command_bus.dispatch.assert_called_once()

        # Verificar comando
        args = mock_command_bus.dispatch.call_args[0]
        command = args[0]
        assert isinstance(command, DeleteHelloWorldCommand)
        assert command.id == 456

    def test_delete_returns_false_when_not_exists(self):
        """Debería retornar False cuando el bus indica fallo."""
        # Arrange
        mock_command_bus = Mock()
        mock_command_bus.dispatch.return_value = False

        use_case = DeleteHelloWorldUseCase(mock_command_bus)

        # Act
        result = use_case.execute(999)

        # Assert
        assert result is False
        mock_command_bus.dispatch.assert_called_once()
