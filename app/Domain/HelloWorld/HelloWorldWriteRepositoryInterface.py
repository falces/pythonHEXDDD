from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.HelloWorld.HelloWorld import HelloWorld


class HelloWorldWriteRepositoryInterface(ABC):
    """
    Interface del repositorio de HelloWorld.
    Define el contrato que debe implementar cualquier repositorio de HelloWorld.
    """

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[HelloWorld]:
        """
        Busca una entidad HelloWorld por su ID.

        Args:
            id: Identificador de la entidad

        Returns:
            HelloWorld: Entidad de dominio o None si no existe
        """
        pass

    @abstractmethod
    def save(self, hello_world: HelloWorld) -> HelloWorld:
        """
        Persiste una entidad HelloWorld.

        Args:
            hello_world: Entidad a persistir

        Returns:
            HelloWorld: Entidad persistida con ID asignado
        """
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """
        Elimina una entidad por su ID.

        Args:
            id: Identificador de la entidad

        Returns:
            bool: True si se eliminó correctamente
        """
        pass
