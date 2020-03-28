from directions import VerticalDirection, LateralDirection, Direction
from view import View
from styles import Styles
from nestedlist import NestedList, NullNestedList


class Model(object):

    __tab: str = "    "

    def __init__(self, view: View, root: NestedList = None):
        """
        Attributes
            max_lines: Maximum visible line count for `result_window`
            __top: Available __top line position for current page (used on scrolling)
            __num_lines(): Available __num_lines() line position for whole pages (as length of items)
            current: Current highlighted line number (as window cursor)
            page: Total page count which being changed corresponding to result of a query (starts from 0)
            ┌--------------------------------------┐
            |1. Item                               |
            |--------------------------------------| <- __top = 1
            |2. Item                               | 
            |3. Item                               |
            |4./Item///////////////////////////////| <- __cursor_y = 3, __abs_cursor_y = 4
            |5. Item                               |
            |6. Item                               |
            |7. Item                               |
            |8. Item                               | <- window_rows = 7, __bottom() = 8
            |--------------------------------------|
            |9. Item                               |
            |10. Item                              | <- __len(lines) = 10
            |                                      |
            |                                      | <- page = 1 (0 and 1)
            └--------------------------------------┘
        """
        self.__view = view
        self.__window_rows, self.__window_cols = self.__view.get_size()
        self.__top = 0
        # current cursor position on window
        self.__cursor_y = 0
        self.__cursor_x = 0
        # Start of Nested List
        if root is None:
            self.__root: NestedList = self.__init_display()
        else:
            self.__root = root
        self.__page = self.__root.count() // self.__window_rows

    @staticmethod
    def __init_display() -> NestedList:
        root = NestedList(["Information about the bean"])
        root.insert_child(["The Bean", "Yes!", "Certainly", "Seldom", "Yum"])
        root.insert_child(["Lima Bean", "Um?", "Totes", "Nope", "Debate-skies"])
        root.insert_child(["This Bean", "I hope", "10/10", "Yep", "1/10"])
        root.insert_child(["Subject", "Good", "Bean-like", "Squidgely", "Grumpy", "Cookery"])
        return root

    @property
    def __bottom(self) -> int:
        """Index of last line currently on screen"""
        return self.__top + self.__window_rows

    @property
    def __abs_cursor_y(self):
        """y axis index of cursor within lines (not screen)"""
        return self.__cursor_y + self.__top

    def __get_node(self, offset: int = 0, start: int = None):
        if start is None:
            start = self.__abs_cursor_y
        return self.__root.get_node(start + offset)

    @property
    def input_char(self) -> int:
        return self.__view.input_char

    def __correct_lateral_bounds(self):
        """
        Puts cursor back in x-axis limits if outside
        """
        node: NestedList = self.__get_node()
        left_limit: int = len(node.indent_padding)
        right_limit: int = node.width
        # put within node
        if self.__cursor_x < left_limit:
            self.__cursor_x = left_limit
        elif self.__cursor_x > right_limit:
            self.__cursor_x = right_limit
        else:  # cursor is within bounds
            field_end = node.get_selected_field_end(self.__cursor_x)
            if field_end < self.__cursor_x:
                # if cursor in padding of field, put it at end
                self.__cursor_x = field_end

    def move(self, direction: Direction, num_spaces: int = 1):
        if isinstance(direction, LateralDirection):
            self.__cursor_x += direction * num_spaces
        else:  # VerticalDirection
            if self.__cursor_y == 0 and direction == VerticalDirection.UP \
                    or self.__cursor_y == self.__window_rows - 1 and direction == VerticalDirection.DOWN:
                # if moving past top or bottom of screen
                self.scroll(direction)
            elif direction == VerticalDirection.UP or self.__abs_cursor_y < self.__root.count() - 1:
                # not moving past bottom of buffer
                self.__cursor_y += direction * num_spaces
        self.__correct_lateral_bounds()

    def move_end(self, direction: LateralDirection):
        spaces = self.__get_node().width
        self.move(direction, spaces)

    def move_field_end(self, direction: LateralDirection):
        node = self.__get_node()
        self.__cursor_x = node.get_selected_field_end(self.__cursor_x)

    def scroll(self, direction: VerticalDirection):
        """Moves the screen up or down
        Prevents the screen moving past the top or bottom of its text
        """
        # if not at absolute top or bottom of lines
        if direction == VerticalDirection.UP and self.__top > 0 \
                or direction == VerticalDirection.DOWN and self.__root.count() > self.__bottom:
            self.__top += direction

    def page(self, direction: VerticalDirection):
        """Paging the window when pressing PgUp/PgDn keys"""
        current_page = (self.__top + self.__cursor_y) // self.__window_rows
        next_page = current_page + direction
        # The last page may have fewer items than max lines,
        # so we should adjust the current cursor position as maximum item count on last page
        if next_page == self.__page:
            self.__cursor_y = min(self.__cursor_y, self.__root.count() % self.__window_rows - 1)

        # Page up
        # if current page is not a first page, page up is possible
        # __top position can not be negative, so if __top position is going to be negative, we should set it as 0
        if (direction == VerticalDirection.UP) and (current_page > 0):
            self.__top = max(0, self.__top - self.__window_rows)
            return
        # Page down
        # if current page is not a last page, page down is possible
        if (direction == VerticalDirection.DOWN) and (current_page < self.__page):
            self.__top += self.__window_rows
            return

    def display(self):
        """Display the items on window"""
        self.__view.clear()
        for abs_row_index, node in enumerate(self.__root):
            if abs_row_index < self.__top:
                # lines before the top of the screen
                continue
            row_index = abs_row_index - self.__top
            if row_index >= self.__window_rows:
                break   # stop at end of window
            # Lines within visible screen
            indent_padding = node.indent_padding
            self.__view.addstr(row_index, 0, indent_padding, Styles.EVEN)
            printed_chars = len(indent_padding)
            for field_index, text in enumerate(node.row_iter):
                """
                style changes between field
                indent precedes first field
                All but last field has trailing tab
                """
                if field_index == 0:
                    style = Styles.HEADER
                elif field_index % 2:
                    style = Styles.EVEN
                else:
                    style = Styles.ODD
                self.__view.addstr(row_index, printed_chars, text, style)
                printed_chars += len(text)
        self.__view.move_cursor(self.__cursor_y, self.__cursor_x)

    def at_root(self):
        return self.__get_node() is self.__root

    def at_line_start(self) -> bool:
        """
        :return: whether the cursor is at the start of the line (past the indent)
        """
        return self.__cursor_x == self.__get_node().indent_padding

    def at_line_end(self):
        """
        :return: whether the cursor is at the start of the line (past the indent)
        """
        return self.__cursor_x == self.__get_node().width

    def at_field_end(self) -> bool:
        return self.__get_node().get_selected_field_end(self.__cursor_x) == self.__cursor_x

    def at_field_start(self) -> bool:
        return self.__get_node().get_selected_field_start(self.__cursor_x) == self.__cursor_x

    def insert(self, insertion: str):
        """
        Insert a string into the current field of the current node
        :param insertion: The string to insert
        """
        node: NestedList = self.__get_node()
        node.insert(self.__cursor_x, insertion)
        self.__cursor_x += len(insertion)

    def delete(self, x_coord_offset: int):
        """
        Delete the character at the given position
        :param x_coord_offset: the offset from the x_coord of the cursor
        """
        node: NestedList = self.__get_node()
        node.delete_char_at(self.__cursor_x + x_coord_offset)
        self.__cursor_x += x_coord_offset

    def is_first_child(self) -> bool:
        """
        :return: whether the cursor's current node is the first child of its parent node
        Vacuously false if current is root.
        """
        current: NestedList = self.__get_node()
        if current is self.__root:
            return False
        previous: NestedList = self.__get_node(-1)
        return previous.child is current

    def indent_current_node(self):
        """
        :precondition: current node cannot be first child or root
        """
        previous: NestedList = self.get_previous_sibling()
        node: NestedList = self.__get_node()
        node.indent(previous)
        self.__cursor_x += len(self.__tab)

    def unindent_current_node(self):
        parent: NestedList = self.get_parent()
        prev_sibling: NestedList = self.get_previous_sibling()
        self.__get_node().unindent(parent, prev_sibling)
        self.__cursor_x -= len(self.__tab)

    def get_previous_sibling(self) -> NestedList:
        """
        :precondition: must not be first child or root
        :return: The previous sibling of the current node
        """
        level = self.__get_node().level
        for index in reversed(range(self.__cursor_y)):
            node = self.__get_node(start=index)
            if node.level == level:
                return node
            if node.level < level:
                return NullNestedList.get_instance()
        raise Exception("no previous sibling or parent found. Is this root?")

    def get_parent(self) -> NestedList:
        """
        Precondition: must not be  level 0 node
        :return: The previous sibling of the current node
        """
        parent_level = self.__get_node().level - 1
        for index in reversed(range(self.__cursor_y)):
            node = self.__get_node(start=index)
            if node.level == parent_level:
                return node
        raise Exception("No parent")

    def split_field(self):
        node = self.__get_node()
        node.split_field(self.__cursor_x)
        self.__cursor_x += node.get_field_padding_len(self.__cursor_x)

    def split_node(self):
        if self.at_line_end() or (not self.at_field_start() and not self.at_field_end()):
            self.split_field()
        if self.at_field_end():
            # cursor needs to be on the first field to move over for node.split()
            self.move(LateralDirection.RIGHT, self.get_padding_len())
        self.__get_node().split(self.__cursor_x)
        self.move(VerticalDirection.DOWN)
        self.move(LateralDirection.LEFT, self.__cursor_x)

    def combine_nodes(self):
        node = self.__get_node()
        assert node.get_level() == 0
        prev_row: NestedList = self.__get_node(offset=-1)
        self.move(VerticalDirection.UP)
        self.move_end(LateralDirection.RIGHT)
        node.combine(prev_row)
        self.move(LateralDirection.RIGHT, self.get_padding_len())

    def get_column_width(self) -> int:
        """
        :return: The width of the column at this field
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return len(node.get_padded_field(field_index))

    def get_neighbor_field(self, direction: LateralDirection) -> str:
        """
        :precondition: cursor cannot currently be in the first field and direction be left
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return node.get_field(field_index + direction)

    def get_padding_len(self) -> int:
        """
        :return: The length of the padding on the current field or the padding that would be on the field if it
        were not the last
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return node.get_padding_len(field_index)

    def get_neighbor_padding_len(self, direction: LateralDirection) -> int:
        """
        :precondition: cursor cannot currently be in the first field and direction be left
        :param direction:
        :return: the number of characters in the padding of the field to the right or left
        of the field inhabited by the cursor
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return node.get_padding_len(field_index + direction)

    def get_neighbor_column_width(self, direction: LateralDirection) -> int:
        """
        :precondition: cursor cannot currently be in the first field and direction be left
        :param direction:
        :return: the number of characters in the padding of the field to the right or left
        of the field inhabited by the cursor
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return len(node.get_padded_field(field_index + direction))

    def combine_fields(self, direction: LateralDirection):
        node = self.__get_node()
        movement = self.get_neighbor_padding_len(direction=LateralDirection.LEFT)
        node.combine_fields(self.__cursor_x, direction)
        if direction == LateralDirection.LEFT:
            self.__cursor_x -= movement

    def signal_user_error(self):
        self.__view.signal_user_error()

    def get_level(self) -> int:
        return self.__get_node().level

