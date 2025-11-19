"""
Tests unitarios para Query Handlers (CQRS).
Valida que las consultas optimizadas funcionen correctamente.
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from Application.Queries.GetAllHelloWorldQuery import GetAllHelloWorldQuery
from Application.Queries.GetHelloWorldByIdQuery import GetHelloWorldByIdQuery
from Application.Queries.SearchHelloWorldQuery import SearchHelloWorldQuery
from Application.QueryHandlers.GetAllHelloWorldHandler import GetAllHelloWorldHandler
from Application.QueryHandlers.GetHelloWorldByIdHandler import GetHelloWorldByIdHandler
from Application.QueryHandlers.SearchHelloWorldHandler import SearchHelloWorldHandler
from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel
from Application.ReadModels.HelloWorldListReadModel import HelloWorldListReadModel


class TestGetAllHelloWorldHandler:
    """Tests para GetAllHelloWorldHandler"""

    def test_handle_returns_paginated_results(self):
        """Debe retornar resultados paginados"""
        # Arrange
        read_models = [
            HelloWorldReadModel(id=1, greeting="Test 1",
                                created_at=datetime.now()),
            HelloWorldReadModel(id=2, greeting="Test 2",
                                created_at=datetime.now()),
        ]

        mock_read_repository = Mock()
        mock_read_repository.find_all = Mock(return_value=read_models)

        handler = GetAllHelloWorldHandler(mock_read_repository)
        query = GetAllHelloWorldQuery(limit=10, offset=0)

        # Act
        result = handler.handle(query)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2

        mock_read_repository.find_all.assert_called_once_with(
            limit=10, offset=0, sort_by='id', sort_order='asc'
        )

    def test_handle_with_custom_sorting(self):
        """Debe aplicar ordenamiento personalizado"""
        # Arrange
        mock_read_repository = Mock()
        mock_read_repository.find_all = Mock(return_value=[])

        handler = GetAllHelloWorldHandler(mock_read_repository)
        query = GetAllHelloWorldQuery(sort_by='greeting', sort_order='desc')

        # Act
        handler.handle(query)

        # Assert
        mock_read_repository.find_all.assert_called_once_with(
            limit=None, offset=None, sort_by='greeting', sort_order='desc'
        )

    def test_handle_with_default_params(self):
        """Debe usar parámetros por defecto"""
        # Arrange
        mock_read_repository = Mock()
        mock_read_repository.find_all = Mock(return_value=[])

        handler = GetAllHelloWorldHandler(mock_read_repository)
        query = GetAllHelloWorldQuery()

        # Act
        result = handler.handle(query)

        # Assert
        assert isinstance(result, list)
        mock_read_repository.find_all.assert_called_once_with(
            limit=None, offset=None, sort_by='id', sort_order='asc'
        )


class TestGetHelloWorldByIdHandler:
    """Tests para GetHelloWorldByIdHandler"""

    def test_handle_returns_read_model_when_found(self):
        """Debe retornar read model cuando encuentra la entidad"""
        # Arrange
        read_model = HelloWorldReadModel(
            id=1,
            greeting="Test",
            created_at=datetime.now()
        )

        mock_read_repository = Mock()
        mock_read_repository.find_by_id = Mock(return_value=read_model)

        handler = GetHelloWorldByIdHandler(mock_read_repository)
        query = GetHelloWorldByIdQuery(id=1)

        # Act
        result = handler.handle(query)

        # Assert
        assert result == read_model
        assert result.id == 1
        assert result.greeting == "Test"
        mock_read_repository.find_by_id.assert_called_once_with(1)

    def test_handle_returns_none_when_not_found(self):
        """Debe retornar None cuando no encuentra la entidad"""
        # Arrange
        mock_read_repository = Mock()
        mock_read_repository.find_by_id = Mock(return_value=None)

        handler = GetHelloWorldByIdHandler(mock_read_repository)
        query = GetHelloWorldByIdQuery(id=999)

        # Act
        result = handler.handle(query)

        # Assert
        assert result is None
        mock_read_repository.find_by_id.assert_called_once_with(999)


class TestSearchHelloWorldHandler:
    """Tests para SearchHelloWorldHandler"""

    def test_handle_searches_with_criteria(self):
        """Debe buscar con criterios específicos"""
        # Arrange
        read_models = [
            HelloWorldReadModel(id=1, greeting="Hello World",
                                created_at=datetime.now()),
        ]

        mock_read_repository = Mock()
        mock_read_repository.search = Mock(return_value=read_models)

        handler = SearchHelloWorldHandler(mock_read_repository)
        query = SearchHelloWorldQuery(search_text="Hello")

        # Act
        result = handler.handle(query)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].greeting == "Hello World"

        mock_read_repository.search.assert_called_once_with(
            search_text="Hello", limit=10, offset=0
        )

    def test_handle_searches_without_criteria(self):
        """Debe buscar sin criterios (retornar todo)"""
        # Arrange
        mock_read_repository = Mock()
        mock_read_repository.search = Mock(return_value=[])

        handler = SearchHelloWorldHandler(mock_read_repository)
        query = SearchHelloWorldQuery()

        # Act
        result = handler.handle(query)

        # Assert
        mock_read_repository.search.assert_called_once_with(
            search_text=None, limit=10, offset=0
        )

    def test_handle_with_pagination(self):
        """Debe aplicar paginación en búsqueda"""
        # Arrange
        mock_read_repository = Mock()
        mock_read_repository.search = Mock(return_value=[])

        handler = SearchHelloWorldHandler(mock_read_repository)
        query = SearchHelloWorldQuery(search_text="Test", limit=5, offset=5)

        # Act
        result = handler.handle(query)

        # Assert
        assert isinstance(result, list)
        mock_read_repository.search.assert_called_once_with(
            search_text="Test", limit=5, offset=5
        )
