from typing import List
from Shared.Application.QueryBus import QueryBus
from Application.Queries.GetAllHelloWorldQuery import GetAllHelloWorldQuery


class GetAllHelloWorldUseCase:
    """
    Caso de Uso para obtener todas las entidades HelloWorld.
    Migrado a CQRS puro: usa QueryBus en lugar del write repository.
    """

    def __init__(self, query_bus: QueryBus):
        self.query_bus = query_bus

    def execute(self) -> List[dict]:
        # 1. Crear query
        query = GetAllHelloWorldQuery()
        
        # 2. Ejecutar query a través del QueryBus
        result = self.query_bus.dispatch(query)
        
        # 3. Retornar lista serializada desde los read models
        # result es List[HelloWorldReadModel]
        return [item.to_dict() for item in result]