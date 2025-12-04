from abc import ABC, abstractmethod
from typing import Optional
from Admin.Domain.User import User


class UserWriteRepositoryInterface(ABC):
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Persiste un usuario (crear o actualizar)."""
        pass
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[User]:
        """Busca un usuario por ID para operaciones de escritura."""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        """Elimina un usuario por ID."""
        pass