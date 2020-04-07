from typing import List
import curses


class Key(object):

    __synonyms = {
        351: [351, 353]
    }

    @property
    def synonyms(self) -> List[int]:
        """
        Return a list of all integer keys that equal this key.
        If there are no synonyms, return a list containing only this integer key
        """
        self.__synonyms.get(self.__key, [self.__key])

    def __init__(self, key: int):
        self.__key: int = key

    def __eq__(self, other):
        if not isinstance(other, Key):
            return False
        return other.__key in self.synonyms

    @classmethod
    def enter(cls):
        return Key(10)

    @classmethod
    def backspace(cls):
        return curses.KEY_BACKSPACE

    @classmethod
    def tab(cls):
        return 9

    @classmethod
    def shift_tab(cls):
        return 351
