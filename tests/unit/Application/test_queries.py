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
        
        assert query.page == 1
        assert query.page_size == 10
        assert query.sort_by == 'id'
        assert query.sort_order == 'asc'
    
    def test_query_with_custom_values(self):
        """Debe crear query con valores personalizados"""
        query = GetAllHelloWorldQuery(
            page=3,
            page_size=25,
            sort_by='greeting',
            sort_order='desc'
        )
        
        assert query.page == 3
        assert query.page_size == 25
        assert query.sort_by == 'greeting'
        assert query.sort_order == 'desc'
    
    def test_query_is_immutable(self):
        """Debe ser inmutable (frozen dataclass)"""
        query = GetAllHelloWorldQuery()
        
        with pytest.raises(AttributeError):
            query.page = 2
    
    def test_query_validates_positive_page(self):
        """Debe rechazar página no positiva"""
        with pytest.raises(ValueError, match="La página debe ser un número positivo"):
            GetAllHelloWorldQuery(page=0)
        
        with pytest.raises(ValueError, match="La página debe ser un número positivo"):
            GetAllHelloWorldQuery(page=-1)
    
    def test_query_validates_page_size_range(self):
        """Debe validar rango de tamaño de página"""
        with pytest.raises(ValueError, match="El tamaño de página debe estar entre 1 y 100"):
            GetAllHelloWorldQuery(page_size=0)
        
        with pytest.raises(ValueError, match="El tamaño de página debe estar entre 1 y 100"):
            GetAllHelloWorldQuery(page_size=101)
    
    def test_query_validates_sort_order(self):
        """Debe validar orden de clasificación"""
        with pytest.raises(ValueError, match="El orden debe ser 'asc' o 'desc'"):
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
        with pytest.raises(ValueError, match="El ID debe ser un número positivo"):
            GetHelloWorldByIdQuery(id=0)
        
        with pytest.raises(ValueError, match="El ID debe ser un número positivo"):
            GetHelloWorldByIdQuery(id=-1)


class TestSearchHelloWorldQuery:
    """Tests para SearchHelloWorldQuery"""
    
    def test_query_with_minimal_data(self):
        """Debe crear query con datos mínimos"""
        query = SearchHelloWorldQuery()
        
        assert query.greeting_contains is None
        assert query.page == 1
        assert query.page_size == 10
    
    def test_query_with_search_criteria(self):
        """Debe crear query con criterios de búsqueda"""
        query = SearchHelloWorldQuery(
            greeting_contains="Hello",
            page=2,
            page_size=20
        )
        
        assert query.greeting_contains == "Hello"
        assert query.page == 2
        assert query.page_size == 20
    
    def test_query_is_immutable(self):
        """Debe ser inmutable (frozen dataclass)"""
        query = SearchHelloWorldQuery(greeting_contains="Test")
        
        with pytest.raises(AttributeError):
            query.greeting_contains = "New"
    
    def test_query_validates_positive_page(self):
        """Debe rechazar página no positiva"""
        with pytest.raises(ValueError, match="La página debe ser un número positivo"):
            SearchHelloWorldQuery(page=0)
    
    def test_query_validates_page_size_range(self):
        """Debe validar rango de tamaño de página"""
        with pytest.raises(ValueError, match="El tamaño de página debe estar entre 1 y 100"):
            SearchHelloWorldQuery(page_size=0)
        
        with pytest.raises(ValueError, match="El tamaño de página debe estar entre 1 y 100"):
            SearchHelloWorldQuery(page_size=101)
