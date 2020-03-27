import curses
from styles import Styles


class View(object):

    @staticmethod
    def signal_user_error():
        curses.beep()

    def __init__(self, window):
        self.__window = window
        curses.init_pair(Styles.ODD, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(Styles.EVEN, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(Styles.HEADER, curses.COLOR_RED, curses.COLOR_BLACK)

    def get_size(self):
        return self.__window.getmaxyx()

    def addstr(self, y: int, x: int, string: str, style: Styles):
        self.__window.addstr(y, x, string, curses.color_pair(style))

    def move_cursor(self, y: int, x: int):
        self.__window.move(y, x)

    def clear(self):
        self.__window.erase()

    def getch(self) -> int:
        return self.__window.input_char()

