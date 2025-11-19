from typing import Optional
from Domain.HelloWorld.HelloWorldRepositoryInterface import HelloWorldRepositoryInterface
from Application.Serializers.HelloWorldSerializer import HelloWorldSerializer


class GetHelloWorldByIdUseCase:
    """
    Caso de Uso: Obtener un HelloWorld por su ID.
    
    Responsabilidades:
    - Buscar la entidad HelloWorld por ID
    - Serializar la entidad si existe
    - Retornar None si no existe
    """
    
    def __init__(self, repository: HelloWorldRepositoryInterface):
        self.repository = repository
    
    def execute(self, hello_world_id: int) -> Optional[dict]:
        """
        Ejecuta el caso de uso de obtener un HelloWorld por ID.
        
        Args:
            hello_world_id: ID del HelloWorld a buscar
            
        Returns:
            dict: HelloWorld encontrado o None si no existe
        """
        # Buscar entidad por ID
        hello_world = self.repository.find_by_id(hello_world_id)
        
        if hello_world is None:
            return None
        
        # Serializar y retornar
        return HelloWorldSerializer.to_dict(hello_world)
