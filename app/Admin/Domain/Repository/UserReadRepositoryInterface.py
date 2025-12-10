from abc import ABC, abstractmethod
from typing import Optional, List
from Admin.Application.ReadModels.UserReadModel import UserReadModel


class UserReadRepositoryInterface(ABC):
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[UserReadModel]:
        """Busca un usuario por ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[UserReadModel]:
        """Obtiene todos los usuarios."""
        pass