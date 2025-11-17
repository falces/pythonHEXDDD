from typing import Dict, List
from Domain.Show.ShowRepositoryInterface import ShowRepositoryInterface
from Infrastructure.ExternalAPI.Mappers.ShowMapper import ShowMapper


class SearchShowsUseCase:
    """
    Caso de Uso: Buscar shows/movies según criterios.
    
    Responsabilidades:
    - Validar los criterios de búsqueda
    - Consultar el repositorio con los criterios
    - Serializar las entidades encontradas
    - Retornar la lista de shows
    """
    
    def __init__(self, repository: ShowRepositoryInterface):
        self.repository = repository
    
    def execute(self, criteria: Dict[str, any]) -> List[dict]:
        """
        Ejecuta el caso de uso de búsqueda de shows.
        
        Args:
            criteria: Diccionario con criterios de búsqueda
                     Ejemplos: {"country": "us", "showType": "movie"}
            
        Returns:
            List[dict]: Lista de shows encontrados en formato diccionario
        """
        # Validar que haya criterios
        if not criteria:
            criteria = {}
        
        # Obtener entidades de dominio desde el repositorio
        shows = self.repository.findByCriteria(criteria)
        
        # Serializar y retornar
        return ShowMapper.toDictList(shows)
