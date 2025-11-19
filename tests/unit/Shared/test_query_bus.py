"""
Tests unitarios para QueryBus (CQRS).
Valida el registro y despacho de queries.
"""

import pytest
from unittest.mock import Mock
from Shared.Application.QueryBus import QueryBus
from Application.Queries.GetAllHelloWorldQuery import GetAllHelloWorldQuery
from Application.Queries.GetHelloWorldByIdQuery import GetHelloWorldByIdQuery
from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel
from datetime import datetime


class TestQueryBus:
    """Tests para QueryBus"""

    def test_register_and_dispatch_query(self):
        """Debe registrar handler y despachar query correctamente"""
        # Arrange
        bus = QueryBus()
        mock_handler = Mock()
        read_model = HelloWorldReadModel(
            id=1, greeting="Test", created_at=datetime.now())
        mock_handler.handle = Mock(return_value=read_model)

        query = GetHelloWorldByIdQuery(id=1)

        # Act
        bus.register(GetHelloWorldByIdQuery, mock_handler)
        result = bus.dispatch(query)

        # Assert
        assert result == read_model
        mock_handler.handle.assert_called_once_with(query)

    def test_dispatch_raises_error_for_unregistered_query(self):
        """Debe lanzar error al despachar query no registrada"""
        # Arrange
        bus = QueryBus()
        query = GetHelloWorldByIdQuery(id=1)

        # Act & Assert
        with pytest.raises(ValueError, match="No handler registered for"):
            bus.dispatch(query)

    def test_register_multiple_queries(self):
        """Debe permitir registrar múltiples tipos de queries"""
        # Arrange
        bus = QueryBus()
        get_all_handler = Mock()
        get_by_id_handler = Mock()

        get_all_query = GetAllHelloWorldQuery()
        get_by_id_query = GetHelloWorldByIdQuery(id=1)

        # Act
        bus.register(GetAllHelloWorldQuery, get_all_handler)
        bus.register(GetHelloWorldByIdQuery, get_by_id_handler)

        bus.dispatch(get_all_query)
        bus.dispatch(get_by_id_query)

        # Assert
        get_all_handler.handle.assert_called_once_with(get_all_query)
        get_by_id_handler.handle.assert_called_once_with(get_by_id_query)

    def test_register_replaces_existing_handler(self):
        """Debe lanzar error al intentar re-registrar handler"""
        # Arrange
        bus = QueryBus()
        old_handler = Mock()
        new_handler = Mock()

        # Act & Assert
        bus.register(GetHelloWorldByIdQuery, old_handler)
        with pytest.raises(ValueError, match="Handler already registered"):
            bus.register(GetHelloWorldByIdQuery, new_handler)

    def test_dispatch_propagates_handler_exceptions(self):
        """Debe propagar excepciones lanzadas por el handler"""
        # Arrange
        bus = QueryBus()
        mock_handler = Mock()
        mock_handler.handle = Mock(side_effect=RuntimeError("Handler error"))

        query = GetHelloWorldByIdQuery(id=1)
        bus.register(GetHelloWorldByIdQuery, mock_handler)

        # Act & Assert
        with pytest.raises(RuntimeError, match="Handler error"):
            bus.dispatch(query)

    def test_query_bus_is_read_only(self):
        """Debe ser usado solo para lecturas (sin side effects)"""
        # Arrange
        bus = QueryBus()
        mock_handler = Mock()
        mock_handler.handle = Mock(return_value=None)

        query = GetHelloWorldByIdQuery(id=1)
        bus.register(GetHelloWorldByIdQuery, mock_handler)

        # Act
        result1 = bus.dispatch(query)
        result2 = bus.dispatch(query)

        # Assert - Multiple dispatches del mismo query no deben alterar estado
        assert result1 == result2
        assert mock_handler.handle.call_count == 2
