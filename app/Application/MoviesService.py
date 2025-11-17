from Domain.Show.ShowRepositoryInterface import ShowRepositoryInterface
from Infrastructure.ExternalAPI.Mappers.ShowMapper import ShowMapper
from typing import Dict, List


class MoviesService:
    """
    Servicio de aplicación para Shows/Movies.
    Orquesta las operaciones de dominio y coordina con el repositorio.
    """
    
    def __init__(
        self,
        repository: ShowRepositoryInterface,
    ):
        # Recibe la instancia del repositorio (Inyección de Dependencias)
        self.repository = repository

    def getMoviesByCriteria(
        self,
        criteria: Dict[str, any],
    ) -> List[dict]:
        """
        Obtiene shows/movies según criterios de búsqueda.
        
        Args:
            criteria: Diccionario con criterios de búsqueda
            
        Returns:
            Lista de shows en formato diccionario
        """
        # Obtener entidades de dominio desde el repositorio
        shows = self.repository.findByCriteria(criteria)
        
        # Convertir entidades a diccionarios para la respuesta
        return ShowMapper.toDictList(shows)
    
    def getShowById(self, show_id: str) -> dict:
        """
        Obtiene un show por su ID.
        
        Args:
            show_id: Identificador del show
            
        Returns:
            Show en formato diccionario o None si no existe
        """
        show = self.repository.findById(show_id)
        
        if show is None:
            return None
        
        return ShowMapper.toDict(show)