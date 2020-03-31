from model import Model
from abc import abstractmethod, ABC


class KeyEffect(ABC):
    @abstractmethod
    def is_relevant(self, model: Model):
        pass

    @abstractmethod
    def execute(self, model: Model):
        pass


class Insert(KeyEffect):
    def is_relevant(self, key: int, model: Model):
        return 31 < key < 127  # printable char range

    def execute(self, key: int, model: Model):
        model.insert(chr(key))
