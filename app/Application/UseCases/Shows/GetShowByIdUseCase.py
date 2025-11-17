from typing import Optional
from Domain.Show.ShowRepositoryInterface import ShowRepositoryInterface
from Infrastructure.ExternalAPI.Mappers.ShowMapper import ShowMapper


class GetShowByIdUseCase:
    """
    Caso de Uso: Obtener un show por su ID.
    
    Responsabilidades:
    - Validar el ID proporcionado
    - Buscar el show en el repositorio
    - Serializar la entidad si existe
    - Retornar None si no existe
    """
    
    def __init__(self, repository: ShowRepositoryInterface):
        self.repository = repository
    
    def execute(self, show_id: str) -> Optional[dict]:
        """
        Ejecuta el caso de uso de obtener un show por ID.
        
        Args:
            show_id: Identificador del show
            
        Returns:
            dict: Show encontrado en formato diccionario o None si no existe
        """
        # Validar que el ID no esté vacío
        if not show_id or len(show_id.strip()) == 0:
            return None
        
        # Buscar el show en el repositorio
        show = self.repository.findById(show_id)
        
        if show is None:
            return None
        
        # Serializar y retornar
        return ShowMapper.toDict(show)
