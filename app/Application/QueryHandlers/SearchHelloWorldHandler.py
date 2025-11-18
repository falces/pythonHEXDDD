"""
Handler para procesar SearchHelloWorldQuery.
"""

from typing import List
from Application.Queries.SearchHelloWorldQuery import SearchHelloWorldQuery
from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel
from Infrastructure.Repository.HelloWorldReadRepository import HelloWorldReadRepository


class SearchHelloWorldHandler:
    """
    Maneja la búsqueda de HelloWorld con criterios.
    """
    
    def __init__(self, read_repository: HelloWorldReadRepository):
        self.read_repository = read_repository
    
    def handle(self, query: SearchHelloWorldQuery) -> List[HelloWorldReadModel]:
        """
        Procesa la query de búsqueda.
        
        Args:
            query: Query con criterios de búsqueda
            
        Returns:
            List[HelloWorldReadModel]: Lista de resultados
        """
        return self.read_repository.search(
            search_text=query.search_text,
            limit=query.limit,
            offset=query.offset
        )
