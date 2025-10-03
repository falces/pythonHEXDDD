from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def findById(self):
        pass

    @abstractmethod
    def findAll(self):
        pass