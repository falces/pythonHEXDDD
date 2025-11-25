from typing import Optional
from Shared.Application.QueryBus import QueryBus
from Application.Queries.GetHelloWorldByIdQuery import GetHelloWorldByIdQuery


class GetHelloWorldByIdUseCase:
    """
    Caso de Uso: Obtener un HelloWorld por su ID.
    Migrado a CQRS puro: usa QueryBus.

    Responsabilidades:
    - Crear la query
    - Despachar la query a través del QueryBus
    - Retornar el resultado serializado
    """

    def __init__(self, query_bus: QueryBus):
        self.query_bus = query_bus

    def execute(self, hello_world_id: int) -> Optional[dict]:
        """
        Ejecuta el caso de uso de obtener un HelloWorld por ID.

        Args:
            hello_world_id: ID del HelloWorld a buscar

        Returns:
            dict: HelloWorld encontrado o None si no existe
        """
        # Crear query
        query = GetHelloWorldByIdQuery(id=hello_world_id)

        # Ejecutar query
        result = self.query_bus.dispatch(query)

        if result is None:
            return None

        # Retornar diccionario (result es HelloWorldReadModel)
        return result.to_dict()
