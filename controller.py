from model import Model
from hotKey import HotKey
import keyboard


class Controller(object):

    def __init__(self, model: Model):
        self.model = model

    def __add_hot_keys(self):
        for subclass in HotKey.__subclasses__():
            instance: HotKey = subclass(self.model)
            instance.add()

    def __input_stream(self):
        """Main loop, waiting on keyboard input"""
        while True:
            self.model.display()
            key: int = self.model.input_char
            if 31 < key < 127:  # printable char range
                self.model.insert(chr(key))

    def run(self):
        """
        Must be called after instantiation
        Continue running the TUI until get interrupted
        """
        self.__add_hot_keys()
        self.__input_stream()
