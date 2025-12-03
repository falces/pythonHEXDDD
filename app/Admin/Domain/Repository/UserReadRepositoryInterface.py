from abc import ABC, abstractmethod
from typing import Optional
from Admin.Application.ReadModels.UserReadModel import UserReadModel


class UserReadRepositoryInterface(ABC):
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[UserReadModel]:
        pass