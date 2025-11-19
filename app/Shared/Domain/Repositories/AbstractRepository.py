from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def find_by_id(self):
        pass

    @abstractmethod
    def find_all(self):
        pass
    
    @abstractmethod
    def find_by_criteria(self):
        pass