from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from Domain.Show.Show import Show


class ShowRepositoryInterface(ABC):
    """
    Interface del repositorio de Show.
    Define el contrato que debe implementar cualquier repositorio de Show.
    
    En este caso, el repositorio consulta una API externa (Stream Availability API)
    en lugar de una base de datos local.
    """

    @abstractmethod
    def find_by_criteria(self, criteria: Dict[str, any]) -> List[Show]:
        """
        Busca shows según criterios específicos.
        
        Args:
            criteria: Diccionario con criterios de búsqueda
                     (ej: {"country": "us", "showType": "movie"})
            
        Returns:
            Lista de entidades Show que cumplen los criterios
        """
        pass

    @abstractmethod
    def find_by_id(self, show_id: str) -> Optional[Show]:
        """
        Busca un show por su ID.
        
        Args:
            show_id: Identificador del show
            
        Returns:
            Show o None si no existe
        """
        pass
