from directions import LateralDirection, VerticalDirection
from model import Model
from typing import List
from keyboard import keyboard
from abc import abstractmethod, ABC
from keyEffect import KeyEffect
import sys


class HotKey(ABC):
    """
    Keys or key combinations that should evoke an effect on the application. The effect may depend on the state of the
    model.
    """

    def __init__(self, model: Model):
        self.__model = model
        self.__key_effects = self._init_key_effects()

    @property
    def model(self) -> Model:
        return self.__model

    @property
    @abstractmethod
    def key_combination(self):
        """
        String or integer representing the combination of keys that should activate the hotkey
        """
        pass

    @property
    def key_effects(self) -> List[KeyEffect]:
        return self.__key_effects

    @abstractmethod
    def _init_key_effects(self) -> List[KeyEffect]:
        pass

    def __get_effect(self) -> KeyEffect:
        class NoEffect(KeyEffect):
            """
            Used if no effect for the given hotkey is appropriate
            Signals to the user that they attempted an unauthorized action
            """
            def is_relevant(self, model: Model) -> bool:
                return False

            def execute(self, model: Model):
                model.signal_user_error()

        # start method
        for effect in self.key_effects:
            if effect.is_relevant(self.model):
                return effect
        return NoEffect()

    def execute(self):
        effect = self.__get_effect()
        effect.execute(self.model)
        self.model.display()

    def add(self):
        keyboard.add_hotkey(self.key_combination, self.execute, suppress=True)


class Tab(HotKey):
    @property
    def key_combination(self):
        return 15

    def _init_key_effects(self) -> List[KeyEffect]:
        class Indent(KeyEffect):
            def is_relevant(self, model: Model):
                return model.at_line_start() and not model.is_first_child()

            def execute(self, model: Model):                model.indent_current_node()

        class Split(KeyEffect):
            def is_relevant(self, model: Model):
                return not model.at_line_start()

            def execute(self, model: Model):
                model.split_field()

        return [Indent(), Split()]


class ShiftTab(HotKey):
    @property
    def key_combination(self) -> str:
        return 'shift+tab'

    def _init_key_effects(self) -> List[KeyEffect]:
        class ShiftTabEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                model.unindent_current_node()

        return [ShiftTabEffect()]


class CtrlEnter(HotKey):
    @property
    def key_combination(self) -> str:
        return 'ctrl+enter'

    def _init_key_effects(self) -> List[KeyEffect]:
        class ToggleCollapse(KeyEffect):
            def is_relevant(self, model: Model) -> bool:
                return model.current_node_has_child

            def execute(self, model: Model):
                model.toggle_current_node_collapsed()

        return [ToggleCollapse()]


class Enter(HotKey):
    @property
    def key_combination(self) -> str:
        return 'enter'

    def _init_key_effects(self) -> List[KeyEffect]:
        class NewLine(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                model.split_node()

        return [NewLine()]


class Backspace(HotKey):
    @property
    def key_combination(self) -> str:
        return 'backspace'

    def _init_key_effects(self) -> List[KeyEffect]:
        class BackspaceNewline(KeyEffect):
            def is_relevant(self, model: Model):
                return model.get_level() == 0 and model.at_line_start() and not model.at_root()

            def execute(self, model: Model):
                model.combine_nodes()

        class UnIndent(KeyEffect):
            def is_relevant(self, model: Model):
                return model.get_level() != 0 and model.at_line_start()

            def execute(self, model: Model):
                model.unindent_current_node()

        class UnSplitBackspace(KeyEffect):
            def is_relevant(self, model: Model):
                return not model.at_line_start() and model.at_field_end(LateralDirection.LEFT)

            def execute(self, model: Model):
                model.combine_fields(LateralDirection.LEFT)

        class TextBackspace(KeyEffect):
            def is_relevant(self, model: Model):
                return not model.at_field_end(LateralDirection.LEFT)

            def execute(self, model: Model):
                model.delete(-1)

        return [BackspaceNewline(), UnIndent(), UnSplitBackspace(), TextBackspace()]


class Delete(HotKey):
    @property
    def key_combination(self) -> str:
        return 'delete'

    def _init_key_effects(self) -> List[KeyEffect]:
        class UnSplitDelete(KeyEffect):
            def is_relevant(self, model: Model):
                return not model.at_line_end() \
                       and model.at_field_end(LateralDirection.RIGHT)

            def execute(self, model: Model):
                model.combine_fields(LateralDirection.RIGHT)

        class TextDelete(KeyEffect):
            def is_relevant(self, model: Model):
                return not model.at_field_end(LateralDirection.RIGHT)

            def execute(self, model: Model):
                model.delete(0)

        return [UnSplitDelete(), TextDelete()]


class PageUp(HotKey):
    @property
    def key_combination(self) -> str:
        return 'Page Up'

    def _init_key_effects(self) -> List[KeyEffect]:
        class PageUpEffect(KeyEffect):
            def is_relevant(self, model: Model) -> bool:
                return True

            def execute(self, model: Model):
                model.page(VerticalDirection.UP)

        return [PageUpEffect()]


class PageDown(HotKey):
    @property
    def key_combination(self) -> str:
        return 'Page Down'

    def _init_key_effects(self) -> List[KeyEffect]:
        class PageDn(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                model.page(VerticalDirection.DOWN)

        return [PageDn()]


class Home(HotKey):
    @property
    def key_combination(self) -> str:
        return 'Home'

    def _init_key_effects(self) -> List[KeyEffect]:
        class HomeEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                model.move_end(LateralDirection.LEFT)

        return [HomeEffect()]


class End(HotKey):
    @property
    def key_combination(self) -> str:
        return 'End'

    def _init_key_effects(self) -> List[KeyEffect]:
        class EndEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                model.move_end(LateralDirection.RIGHT)

        return [EndEffect()]


class Up(HotKey):
    @property
    def key_combination(self) -> str:
        return 'Up'

    def _init_key_effects(self) -> List[KeyEffect]:
        class UpEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                model.move(VerticalDirection.UP)

        return [UpEffect()]


class Left(HotKey):
    @property
    def key_combination(self) -> str:
        return 'Left'

    def _init_key_effects(self) -> List[KeyEffect]:
        class LeftEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                model.move(LateralDirection.LEFT)

        return [LeftEffect()]


class Right(HotKey):
    @property
    def key_combination(self) -> str:
        return 'Right'

    def _init_key_effects(self) -> List[KeyEffect]:
        class RightEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                padding_len: int = model.get_padding_len()
                if model.at_field_end(LateralDirection.RIGHT):
                    num_spaces = padding_len
                else:
                    num_spaces = 1
                model.move(LateralDirection.RIGHT, num_spaces)

        return [RightEffect()]


class Down(HotKey):
    @property
    def key_combination(self) -> str:
        return 'Down'

    def _init_key_effects(self) -> List[KeyEffect]:
        class DownEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                model.move(VerticalDirection.DOWN)

        return[DownEffect()]


class CtrlLeft(HotKey):
    @property
    def key_combination(self) -> str:
        return 'ctrl + left'

    def _init_key_effects(self) -> List[KeyEffect]:
        class CtrlLeftEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                left = LateralDirection.LEFT
                if model.at_field_end(left):
                    model.move(left, model.get_neighbor_column_width(left))
                else:
                    model.move_field_end(left)

        return [CtrlLeftEffect()]


class CtrlRight(HotKey):
    @property
    def key_combination(self) -> str:
        return 'ctrl + right'

    def _init_key_effects(self) -> List[KeyEffect]:
        class CtrlRightEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return not model.at_line_end()

            def execute(self, model: Model):
                right = LateralDirection.RIGHT
                if model.at_field_end(right):
                    model.move(right, model.get_padding_len() + len(model.get_neighbor_field(right)))
                else:
                    model.move_field_end(right)

        return [CtrlRightEffect()]


class Esc(HotKey):
    @property
    def key_combination(self) -> str:
        return 'esc'

    def _init_key_effects(self) -> List[KeyEffect]:
        class EscEffect(KeyEffect):
            def is_relevant(self, model: Model):
                return True

            def execute(self, model: Model):
                sys.exit()

        return [EscEffect()]


class CtrlS(HotKey):
    @property
    def key_combination(self) -> str:
        return 'ctrl+s'

    def _init_key_effects(self) -> List[KeyEffect]:
        class Save(KeyEffect):
            def is_relevant(self, model: Model) -> bool:
                return True

            def execute(self, model: Model):
                model.save()
        return [Save()]