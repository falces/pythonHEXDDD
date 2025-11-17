from typing import List
from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Infrastructure.Persistence.Mappers.HelloWorldMapper import HelloWorldMapper


class GetAllHelloWorldUseCase:
    """
    Caso de Uso para obtener todas las entidades HelloWorld.
    Su única responsabilidad es consultar y serializar la lista.
    """

    def __init__(self, repository: HelloWorldRepositoryInterface):
        self.repository = repository

    def execute(self) -> List[dict]:
        # 1. Obtener todas las entidades desde el repositorio
        entities = self.repository.findAll()
        # 2. Serializar cada entidad a un diccionario
        return [HelloWorldMapper.toDict(e) for e in entities]