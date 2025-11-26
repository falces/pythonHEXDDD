"""
Handler para procesar GetHelloWorldByIdQuery.
"""

from typing import Optional
from Application.Queries.GetHelloWorldByIdQuery import GetHelloWorldByIdQuery
from Application.ReadModels.HelloWorldReadModel import HelloWorldReadModel
from Domain.HelloWorld.HelloWorldReadRepositoryInterface import HelloWorldReadRepositoryInterface
from Shared.Application.QueryHandler import QueryHandler


class GetHelloWorldByIdHandler(QueryHandler):
    """
    Maneja la consulta de HelloWorld por ID.
    Usa repositorio de lectura optimizado.
    """

    def __init__(self, read_repository: HelloWorldReadRepositoryInterface):
        self.read_repository = read_repository

    def handle(self, query: GetHelloWorldByIdQuery) -> Optional[HelloWorldReadModel]:
        """
        Procesa la query de buscar por ID.

        Args:
            query: Query con el ID a buscar

        Returns:
            HelloWorldReadModel o None si no existe
        """
        return self.read_repository.find_by_id(query.id)
