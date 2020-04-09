from model import Model
from abc import abstractmethod, ABC


class KeyEffect(ABC):
    @abstractmethod
    def is_relevant(self, model: Model) -> bool:
        pass

    @abstractmethod
    def execute(self, model: Model):
        pass
