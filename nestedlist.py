from typing import List
from directions import LateralDirection
from simpleNestedList import SimpleNestedList


class NestedList(SimpleNestedList):

    def __init__(self):
        super().__init__()
        # are the children hidden
        self.__collapsed = False

    def __str__(self) -> str:
        """
        For debugging and testing
        :return: string representation of Nested List starting from this node
        """
        to_return = self.indent_padding
        for text in self.row_iter:
            to_return += text
        to_return += "\n"
        to_return += str(self.child)
        to_return += str(self.sibling)
        return to_return

    def __iter__(self):
        return NestedListIterator(self)

    def __len__(self) -> int:
        raise Exception("This used to mean width")

    def _get_field_index(self, x_coord: int) -> int:
        """
        :param x_coord:
        :return: index of field that the x_coordinate falls within
        """
        x_coord -= len(self.indent_padding)
        for index, field in enumerate(self.row_iter):
            ext_length = len(field)
            if x_coord < ext_length:
                return index
            x_coord -= ext_length
        raise IndexError("x_cord {} space out of bounds to the right".format(x_coord))

    def get_selected_field(self, x_coord) -> str:
        return self._get_field(self._get_field_index(x_coord))

    def __get_field_start(self, field_index: int) -> int:
        """
        :param field_index: Which field to get the start of
        :return: The x-coord of the start of the field at the given index
        """
        assert 0 <= field_index < self.num_fields
        count = len(self.indent_padding)
        for i, field in enumerate(self.row_iter):
            if i == field_index:
                return count
            count += len(field)
        raise Exception("Unreachable")

    def get_selected_field_start(self, x_coord: int) -> int:
        field_index = self._get_field_index(x_coord)
        return self.__get_field_start(field_index)

    def __get_field_end(self, field_index: int) -> int:
        """
        :param field_index: Which field to get the end of
        :return: The x-coord of the end of the field at the given index
        """
        start = self.__get_field_start(field_index)
        return start + len(self._get_field(field_index))

    def get_selected_field_end(self, x_coord: int) -> int:
        field_index = self._get_field_index(x_coord)
        return self.__get_field_end(field_index)

    def __get_index_in_field(self, x_coord: int) -> int:
        """
        :param x_coord:
        :return: the relative position from the start of a field the coordinate is in
            FIELD: "FIELD1    "FIELD2
                    01234567890123456
            get_rel_field_index(3) == 3
            get_rel_field_index(12) == 1
        """
        x_coord -= len(self.indent_padding)
        for index, field in enumerate(self.row_iter):
            ext_length = len(field)
            if x_coord < ext_length:
                return x_coord
            x_coord -= ext_length
        raise IndexError("x_cord {} space right out of bounds".format(x_coord))

    @property
    def null(self):
        return NullNestedList.get_instance()

    def get_last_sibling(self):
        """
        :return: Last sibling on this level of a nested list
        """
        if self.sibling is self.null:
            return self
        return self.sibling.get_last_sibling()

    def get_last_child(self):
        return self.__child.get_last_sibling()

    """
    def get_text_len(self, x_coord: int) -> int:
        return self._get_field(x_coord).get_text_len()

    def get_neighbor_text_len(self, x_coord: int, direction: LateralDirection) -> int:
        neighbor: _Field = self.__get_neighbor_field(x_coord, direction)
        return neighbor.get_text_len()

    def get_field_padding_len(self, x_coord: int) -> int:
        return self._get_field(x_coord).get_padding_len()

    def get_neighbor_field_padding_len(self, x_coord: int, direction: LateralDirection) -> int:
        neighbor: _Field = self.__get_neighbor_field(x_coord, direction)
        return neighbor.get_padding_len()

    def get_column_width(self, x_coord: int) -> int:
        return len(self._get_field(x_coord))

    def get_neighbor_column_width(self, x_coord: int, direction: LateralDirection) -> int:
        neighbor: _Field = self.__get_neighbor_field(x_coord, direction)
        return len(neighbor)

    def get_indent_len(self):
        return self.__tab_size * self.__level
    """
    def get_node(self, row: int):
        """
        :param row: the row the returned NestedList starts at relative to this node
        :returns: the NestedList that starts at row. None if out of bounds
        """
        if row == 0:
            return self
        row -= 1
        child_count = self.child.count()
        if row < child_count:
            return self.child.get_node(row)
        row -= child_count
        sibling_count = self.sibling.count()
        if row < sibling_count:
            return self.sibling.get_node(row)
        raise IndexError("index is {} past end of NestedList".format(row))

    def count(self) -> int:
        """
        :return: the number of NestedList nodes starting from and including this
        skipping all collapsed children
        """
        nodes: int = 1
        if not self.__collapsed:
            nodes += self.__child.count()
        nodes += self.__sibling.count()
        return nodes

    """
    Field Editing
    """

    def insert(self, x_coord, insertion: str):
        """inserts a string into a pre-existing field"""
        field_index = self._get_field_index(x_coord)
        field: str = self._get_field(field_index)
        index = self.__get_index_in_field(x_coord)
        new_text = field[0:index] + insertion + field[index:len(field)]
        self.replace_field(field_index, new_text)

    def delete_char_at(self, x_coord: int):
        field_index = self._get_field_index(x_coord)
        field: str = self._get_field(field_index)
        index = self.__get_index_in_field(x_coord)
        new_text = field[0:index] + field[index + 1:len(field)]
        self.replace_field(field_index, new_text)

    def split_field(self, x_coord: int):
        field_index = self._get_field_index(x_coord)
        field_to_split = self._get_field(field_index)
        split_index = self.__get_index_in_field(x_coord)
        left_text = field_to_split[0:split_index]
        right_text = field_to_split[split_index:]
        self.replace_field(field_index, left_text)
        self.insert_field(field_index + 1, right_text)

    """
    Edit Node
    """

    def indent(self, prev_sibling: SimpleNestedList):
        """
        makes this node's sibling his child, and its sibling's sibling, its sibling
        """
        assert prev_sibling is not self.null
        prev_sibling.insert_child(self.fields)
        del prev_sibling.sibling

    def unindent(self, parent: SimpleNestedList):
        """
        :param parent: The parent of this node or one of its older siblings
        """
        assert parent is not self.null
        new_self = parent.insert_sibling(self.fields)
        new_self._copy_family(self)
        del self

    def _copy_family(self, copy_from):
        """
        recursively copies the children and siblings from copy_from onto self
        :param copy_from:
        """
        self.insert_sibling(copy_from.sibling.fields)
        self.sibling._copy_family(copy_from.sibling)
        self.insert_child(copy_from.child.fields)
        self.child._copy_family(copy_from.child)

    def split(self, x_coord: int):
        """
        Create a new node as a sibling with all fields right of the x_coord, inclusive
        These fields are removed from this node
        Does not split the field itself, only the row
        :param x_coord: The row is split at the field containing the x_coord
        """
        field_index = self._get_field_index(x_coord)
        split_fields: List[str] = []
        for index, field in enumerate(self.row_iter, start = field_index):
            split_fields.append(field)
            self.delete_field(index)
        self.insert_sibling(split_fields)

    """
    def give_fields(self, prev_row, prev_sibling):
        assert prev_row is not None
        prev_sibling._set_sibling(self.__sibling)
        last_child = prev_sibling.get_last_child()
        if last_child is self.__null():
            prev_sibling._set_child(self.__child)
        else:
            last_child._set_sibling(self.__child)
        for field in self.__fields:
            prev_row.append_field(field.get_text())
    """

    def combine_fields(self, x_coord: int, direction: LateralDirection):
        field_index = self._get_field_index(x_coord)
        current_field = self._get_field(field_index)
        other_field = self._get_field(field_index + direction)
        if direction == LateralDirection.LEFT:
            left_field = other_field
            right_field = current_field
            right_field_index = field_index
        else:
            left_field = current_field
            right_field = other_field
            right_field_index = field_index + direction
        self.replace_field(right_field_index - 1, left_field+right_field)
        self.delete_field(right_field_index)

    def append_field(self, text: str):
        self.insert_field(text, len(self.__fields))


class NestedListIterator:
    def __init__(self, root: NestedList):
        # fake node parenting root
        first = NestedList.new_node("    ", level=0, first_child=root, columns=[])
        self.previous: List[NestedList] = [first]

    def __next__(self):
        next_node = self.previous[-1].get_child()
        if not isinstance(next_node, NullNestedList):
            self.previous.append(next_node)
            return next_node
        while len(self.previous) > 0:
            next_node = self.previous.pop().get_sibling()
            if not isinstance(next_node, NullNestedList):
                self.previous.append(next_node)
                return next_node
        raise StopIteration


class NullNestedList(NestedList):
    """
    Marks the ends of Nested List branches
    Vacuously implements all NestedList methods
    """
    __instance = None

    @staticmethod
    def get_instance():
        if NullNestedList.__instance is None:
            NullNestedList.__instance = NullNestedList()
        return NullNestedList.__instance

    def __init__(self):
        """private constructor"""
        if NullNestedList.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            NullNestedList.__instance = self

    def __eq__(self, other) -> bool:
        return other is self

    def __len__(self) -> int:
        return 0

    def __str__(self) -> str:
        return ''

    @property
    def _columns(self):
        """
        For creating a new array of columns when the new node has no sibling
        """
        return []

    @property
    def child(self):
        return self

    @property
    def sibling(self):
        return self

    @property
    def level(self):
        raise Exception("Not allowed for NullRow")

    @property
    def copy_family(self):
        pass

    def get_last_sibling(self, stop_before=None):
        return self

    def get_last_child(self, stop_before=None):
        raise Exception("Should not be called on a NullNestedList")

    def get_node(self, row: int):
        raise Exception("Should not be called on a NullNestedList")

    def count(self) -> int:
        return 0

    def new_child(self, texts: List[str] = None):
        raise Exception("Should not be called on a NullNestedList")

    def new_sibling(self, fields: List[str] = None):
        raise Exception("Should not be called on a NullNestedList")

    def delete_first_child(self):
        raise Exception("Should not be called on a NullNestedList")

    def delete_next_sibling(self):
        raise Exception("Should not be called on a NullNestedList")

    def insert(self, x_coord, insertion: str):
        raise Exception("Should not be called on a NullNestedList")

    def insert_field(self, text: str, insert_index: int):
        raise Exception("Should not be called on a NullNestedList")

    def split(self, x_coord: int):
        raise Exception("Should not be called on a NullNestedList")

    def split_field(self, x_coord: int):
        raise Exception("Should not be called on a NullNestedList")

    def _append_child(self, new_child):
        raise Exception("Should not be called on a NullNestedList")
