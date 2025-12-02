from abc import ABC, abstractmethod
from typing import Optional


class UserReadRepositoryInterface(ABC):
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[any]:
        pass