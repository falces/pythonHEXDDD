"""
Handler para procesar GetAllHelloWorldQuery.
"""

from typing import List
from Application.Queries.GetAllHelloWorldQuery import GetAllHelloWorldQuery
from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel
from Infrastructure.Repository.HelloWorldReadRepository import HelloWorldReadRepository


class GetAllHelloWorldHandler:
    """
    Maneja la consulta de todos los HelloWorld.
    Usa repositorio de lectura optimizado.
    """
    
    def __init__(self, read_repository: HelloWorldReadRepository):
        self.read_repository = read_repository
    
    def handle(self, query: GetAllHelloWorldQuery) -> List[HelloWorldReadModel]:
        """
        Procesa la query de obtener todos.
        
        Args:
            query: Query con parámetros de filtrado/paginación
            
        Returns:
            List[HelloWorldReadModel]: Lista de read models
        """
        return self.read_repository.find_all(
            limit=query.limit,
            offset=query.offset,
            sort_by=query.sort_by,
            sort_order=query.sort_order
        )
