"""
Tests unitarios para Queries (CQRS).
Valida que las queries sean inmutables y validen correctamente.
"""

import pytest
from Application.Queries.GetAllHelloWorldQuery import GetAllHelloWorldQuery
from Application.Queries.GetHelloWorldByIdQuery import GetHelloWorldByIdQuery
from Application.Queries.SearchHelloWorldQuery import SearchHelloWorldQuery


class TestGetAllHelloWorldQuery:
    """Tests para GetAllHelloWorldQuery"""

    def test_query_with_default_values(self):
        """Debe crear query con valores por defecto"""
        query = GetAllHelloWorldQuery()

        assert query.limit is None
        assert query.offset is None
        assert query.sort_by == 'id'
        assert query.sort_order == 'asc'

    def test_query_with_custom_values(self):
        """Debe crear query con valores personalizados"""
        query = GetAllHelloWorldQuery(
            limit=25,
            offset=50,
            sort_by='greeting',
            sort_order='desc'
        )

        assert query.limit == 25
        assert query.offset == 50
        assert query.sort_by == 'greeting'
        assert query.sort_order == 'desc'

    def test_query_is_immutable(self):
        """Debe ser inmutable (frozen dataclass)"""
        query = GetAllHelloWorldQuery()

        with pytest.raises(AttributeError):
            query.limit = 2

    def test_query_validates_positive_limit(self):
        """Debe rechazar limit no positivo"""
        with pytest.raises(ValueError, match="limit must be a positive integer"):
            GetAllHelloWorldQuery(limit=0)

        with pytest.raises(ValueError, match="limit must be a positive integer"):
            GetAllHelloWorldQuery(limit=-1)

    def test_query_validates_non_negative_offset(self):
        """Debe validar que offset no sea negativo"""
        with pytest.raises(ValueError, match="offset must be a non-negative integer"):
            GetAllHelloWorldQuery(offset=-1)

    def test_query_validates_sort_order(self):
        """Debe validar orden de clasificación"""
        with pytest.raises(ValueError, match="sort_order must be 'asc' or 'desc'"):
            GetAllHelloWorldQuery(sort_order='invalid')


class TestGetHelloWorldByIdQuery:
    """Tests para GetHelloWorldByIdQuery"""

    def test_query_with_valid_id(self):
        """Debe crear query con ID válido"""
        query = GetHelloWorldByIdQuery(id=1)

        assert query.id == 1

    def test_query_is_immutable(self):
        """Debe ser inmutable (frozen dataclass)"""
        query = GetHelloWorldByIdQuery(id=1)

        with pytest.raises(AttributeError):
            query.id = 2

    def test_query_validates_positive_id(self):
        """Debe rechazar ID no positivo"""
        with pytest.raises(ValueError, match="id must be a positive integer"):
            GetHelloWorldByIdQuery(id=0)

        with pytest.raises(ValueError, match="id must be a positive integer"):
            GetHelloWorldByIdQuery(id=-1)


class TestSearchHelloWorldQuery:
    """Tests para SearchHelloWorldQuery"""

    def test_query_with_minimal_data(self):
        """Debe crear query con datos mínimos"""
        query = SearchHelloWorldQuery()

        assert query.search_text is None
        assert query.limit == 10
        assert query.offset == 0

    def test_query_with_search_criteria(self):
        """Debe crear query con criterios de búsqueda"""
        query = SearchHelloWorldQuery(
            search_text="Hello",
            limit=20,
            offset=10
        )

        assert query.search_text == "Hello"
        assert query.limit == 20
        assert query.offset == 10

    def test_query_is_immutable(self):
        """Debe ser inmutable (frozen dataclass)"""
        query = SearchHelloWorldQuery(search_text="Test")

        with pytest.raises(AttributeError):
            query.search_text = "New"

    def test_query_validates_positive_limit(self):
        """Debe rechazar limit no positivo"""
        with pytest.raises(ValueError, match="limit must be a positive integer"):
            SearchHelloWorldQuery(limit=0)

    def test_query_validates_non_negative_offset(self):
        """Debe validar que offset no sea negativo"""
        with pytest.raises(ValueError, match="offset must be a non-negative integer"):
            SearchHelloWorldQuery(offset=-1)
