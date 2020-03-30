from model import Model
from directions import VerticalDirection, LateralDirection
from abc import abstractmethod, ABC
import curses
import curses.ascii
import keyboard

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


class Commands(object):
    # contains all subclasses oh KeyCommand
    __key_commands = []

    @classmethod
    def __get_key_commands(cls):
        if len(cls.__key_commands) == 0:
            for subclass in KeyEffect.__subclasses__():
                cls.__key_commands.append(subclass())
        return cls.__key_commands

    @classmethod
    def __get_command(cls, key: int, model: Model) -> KeyEffect:
        for command in Commands.__get_key_commands():
            if command.is_relevant(key, model):
                return command
        raise Exception("No relevant command")

    @classmethod
    def execute(cls, key: int, model: Model):
        command = Commands.__get_command(key, model)
        command.execute(key, model)
