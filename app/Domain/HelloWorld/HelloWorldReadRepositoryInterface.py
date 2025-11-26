"""
Interface del repositorio de lectura de HelloWorld.
Define el contrato para operaciones de lectura en CQRS.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class HelloWorldReadRepositoryInterface(ABC):
    """
    Interface del repositorio de lectura de HelloWorld.
    
    En CQRS, las operaciones de lectura están separadas de las de escritura.
    Esta interfaz define el contrato para consultas optimizadas.
    
    Note:
        Los métodos retornan ReadModels, no entidades de dominio,
        ya que las lecturas no necesitan comportamiento de dominio.
    """

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[any]:
        """
        Busca un HelloWorld por su ID.
        
        Args:
            id: Identificador único
            
        Returns:
            ReadModel o None si no existe
        """
        pass

    @abstractmethod
    def find_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: str = 'id',
        sort_order: str = 'asc'
    ) -> List[any]:
        """
        Obtiene todos los HelloWorld con paginación y ordenamiento.
        
        Args:
            limit: Número máximo de resultados
            offset: Desplazamiento para paginación
            sort_by: Campo por el cual ordenar
            sort_order: Dirección del ordenamiento ('asc' o 'desc')
            
        Returns:
            Lista de ReadModels
        """
        pass

    @abstractmethod
    def search(
        self,
        search_text: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[any]:
        """
        Busca HelloWorld según criterios de búsqueda.
        
        Args:
            search_text: Texto a buscar en el greeting
            limit: Número máximo de resultados
            offset: Desplazamiento para paginación
            
        Returns:
            Lista de ReadModels que coinciden
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Cuenta el total de registros.
        
        Returns:
            Total de HelloWorld
        """
        pass
