from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        """Todo comando deve ter um método execute."""
        pass