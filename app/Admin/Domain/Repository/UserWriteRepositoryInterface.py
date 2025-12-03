from abc import ABC, abstractmethod
from Admin.Domain.User import User


class UserWriteRepositoryInterface(ABC):
    
    @abstractmethod
    def save(
        self,
        user: User,
    ) -> User:
        pass