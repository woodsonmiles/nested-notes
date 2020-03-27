from model import Model
from directions import VerticalDirection, LateralDirection
from abc import abstractmethod
from abc import ABC
import curses
import curses.ascii
import sys


class KeyCommand(ABC):
    @abstractmethod
    def is_relevant(self, key: int, model: Model):
        pass

    @abstractmethod
    def execute(self, key: int, model: Model):
        pass


class NewLine(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == 10

    def execute(self, key: int, model: Model):
        model.split_node()


class BackspaceNewline(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return model.get_level() == 0 and key == curses.KEY_BACKSPACE and model.at_line_start() and not model.at_root()

    def execute(self, key: int, model: Model):
        model.combine_nodes()


class IndentTab(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == 9 and model.at_line_start() and not model.is_first_child()

    def execute(self, key: int, model: Model):
        model.indent_current_node()


class SplitTab(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == 9 and not model.at_line_start()

    def execute(self, key: int, model: Model):
        model.split_field()


class UnIndent(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return model.get_level() != 0 and key == curses.KEY_BACKSPACE and model.at_line_start()

    def execute(self, key: int, model: Model):
        model.unindent_current_node()


class UnSplitBackspace(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_BACKSPACE and not model.at_line_start() and model.at_field_start()

    def execute(self, key: int, model: Model):
        model.combine_fields(LateralDirection.LEFT)


class UnSplitDelete(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_DC and not model.at_line_end() \
               and model.at_field_end()

    def execute(self, key: int, model: Model):
        model.combine_fields(LateralDirection.RIGHT)


class Insert(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return 31 < key < 127  # printable char range

    def execute(self, key: int, model: Model):
        model.insert(chr(key))


class TextBackspace(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_BACKSPACE and not model.at_field_start()

    def execute(self, key: int, model: Model):
        model.delete(-1)


class TextDelete(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_DC and not model.at_field_end()

    def execute(self, key: int, model: Model):
        model.delete(0)


class PageUp(KeyCommand):
    def is_relevant(self, key: int, model: Model) -> bool:
        return key == curses.KEY_PPAGE

    def execute(self, key, model: Model):
        model.page(VerticalDirection.UP)


class Home(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_HOME

    def execute(self, key: int, model: Model):
        model.move_end(LateralDirection.LEFT)


class End(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_END

    def execute(self, key: int, model: Model):
        model.move_end(LateralDirection.RIGHT)


class PageDn(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_NPAGE

    def execute(self, key: int, model: Model):
        model.page(VerticalDirection.DOWN)


class Up(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_UP

    def execute(self, key: int, model: Model):
        model.move(VerticalDirection.UP)


class Left(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_LEFT

    def execute(self, key: int, model: Model):
        model.move(LateralDirection.LEFT)


class Right(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_RIGHT

    def execute(self, key: int, model: Model):
        padding_len: int = model.get_padding_len()
        if model.at_field_end():
            num_spaces = padding_len
        else:
            num_spaces = 1
        model.move(LateralDirection.RIGHT, num_spaces)


class CtrLeft(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == 545

    def execute(self, key: int, model: Model):
        left = LateralDirection.LEFT
        if model.at_field_start():
            model.move(left, model.get_neighbor_column_width(left))
        else:
            model.move_field_end(left)


class CtrRight(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == 560

    def execute(self, key: int, model: Model):
        right = LateralDirection.RIGHT
        if model.at_field_end():
            model.move(right, model.get_padding_len() + len(model.get_neighbor_field(right)))
        else:
            model.move_field_end(right)


class Down(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.KEY_DOWN

    def execute(self, key: int, model: Model):
        model.move(VerticalDirection.DOWN)


class Esc(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == curses.ascii.ESC

    def execute(self, key: int, model: Model):
        sys.exit()


class UserError(KeyCommand):
    """
    Precondition: All other KeyCommand subclasses are checked (is_relevant()) before this is run
    This must remain the last subclass of KeyCommand
    listed below the others in this file.
    """
    def is_relevant(self, key: int, model: Model):
        return True

    def execute(self, key: int, model: Model):
        model.signal_user_error()


class Commands(object):
    # contains all subclasses oh KeyCommand
    __key_commands = []

    @classmethod
    def __get_key_commands(cls):
        if len(cls.__key_commands) == 0:
            for subclass in KeyCommand.__subclasses__():
                cls.__key_commands.append(subclass())
        return cls.__key_commands

    @classmethod
    def __get_command(cls, key: int, model: Model) -> KeyCommand:
        for command in Commands.__get_key_commands():
            if command.is_relevant(key, model):
                return command
        raise Exception("No relevant command")

    @classmethod
    def execute(cls, key: int, model: Model):
        command = Commands.__get_command(key, model)
        command.execute(key, model)
