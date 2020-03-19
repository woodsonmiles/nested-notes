from typing import List
from directions import LateralDirection


class NestedList(object):

    def __init__(self, tab: str, fields: List[str] = None):
        self.__tab = tab
        self.__tab_size = len(tab)
        self.__row = Row(tab, fields)

    def __str__(self) -> str:
        """
        For debugging and testing
        :return: string representation of Nested List starting from this node
        """
        to_return = self.get_indent()
        for text in self.get_texts():
            to_return += text
        to_return += "\n"
        to_return += str(self.get_child())
        to_return += str(self.get_sibling())
        return to_return

    def __eq__(self, other) -> bool:
        return isinstance(other, NestedList) and \
               self.__fields == other.__fields and \
               self.__child == other.__child and \
               self.__sibling == other.__sibling

    def __iter__(self):
        return NestedListIterator(self)

    def __len__(self) -> int:
        """
        :return: num characters in string representation of fields including indentation and separation
        """
        # TODO - error if no fields and moving up into an empty previous row
        total = self.get_indent_len()
        for field in self.__fields:
            total += len(field)
        if len(self.__fields) > 0:
            total -= self.__fields[-1].get_padding_len()
        return total

    def _decrement_level(self):
        self.__level -= 1
        self.__child._decrement_level()
        self.__sibling._decrement_level()

    def _get_field(self, x_coord: int) -> _Field:
        """
        :param x_coord:
        :return: field that the x_coordinate falls within
        """
        x_coord -= self.__tab_size * self.__level
        for field in self.__fields:
            ext_length = len(field)
            if x_coord < ext_length:
                return field
            x_coord -= ext_length
        raise IndexError("x_cord {} space out of bounds to the right".format(x_coord))

    def _get_field_index(self, x_coord: int) -> int:
        """
        :param x_coord:
        :return: index of field that the x_coordinate falls within
        """
        x_coord -= self.__tab_size * self.__level
        for index, field in enumerate(self.__fields):
            ext_length = len(field)
            if x_coord < ext_length:
                return index
            x_coord -= ext_length
        raise IndexError("x_cord {} space out of bounds to the right".format(x_coord))

    def __get_neighbor_field(self, x_coord: int, direction: LateralDirection) -> _Field:
        current_index = self._get_field_index(x_coord)
        neighbor_index = current_index + direction
        assert neighbor_index > -1
        assert neighbor_index < len(self.__fields)
        return self.__fields[neighbor_index]

    @staticmethod
    def __null():
        return NullNestedList.get_instance()



    def indent(self, prev_sibling):
        """
        makes this node's sibling his child, and its sibling's sibling, its sibling
        :precondition: this should not have a pre-existing child
        """
        # TODO - columns not updated, make update columns method
        prev_sibling.__append_child(self)
        prev_sibling.__set_sibling(self.get_sibling())
        self.__set_sibling(self.get_child())
        self.__child = NullNestedList.get_instance()
        self.__level += 1

    def unindent(self, parent, prev_sibling):
        """
        :param parent: Not Null
        :param prev_sibling: NullNestedList if no previous sibling
        """
        # TODO - columns not updated
        if parent.__child is self:
            parent.__child = NullNestedList.get_instance()
        else:  # has prev sibling
            prev_sibling.__sibling = NullNestedList.get_instance()
        old_sibling = self.__sibling
        self.__sibling = parent.get_sibling()
        parent.__sibling = self
        self.__level -= 1
        if isinstance(self.__child, NullNestedList):
            self.__child = old_sibling
        else:
            self.__child._decrement_level()
            self.get_last_child()._set_sibling(old_sibling)

    def get_last_sibling(self):
        """
        :return: Last sibling on this level of a nested list
        """
        if self.__sibling is NestedList.__null():
            return self
        return self.__sibling.get_last_sibling()

    def get_last_child(self):
        return self.__child.get_last_sibling()

    def replace_field(self, index: int, new_text: str):
        self.__fields[index].replace_text(new_text)

    def get_rel_field_index(self, x_coord: int) -> int:
        """
        :param x_coord:
        :return: the relative position from the start of a field the coordinate is in
            FIELD: "FIELD1    "FIELD2
                    01234567890123456
            get_rel_field_index(3) == 3
            get_rel_field_index(12) == 1
        """
        x_coord -= self.__level * self.__tab_size
        for index, field in enumerate(self.__fields):
            ext_length = len(field)
            if x_coord < ext_length:
                return x_coord
            x_coord -= ext_length
        raise IndexError("x_cord {} space right out of bounds".format(x_coord))

    def get_indent(self):
        return self.__level * self.__tab

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

    def get_texts(self):
        class FieldIter(object):
            def __init__(self, fields: List[_Field]):
                self.fields = fields
                self._num_fields = len(fields)
                self.__count = 0

            def __iter__(self):
                return self

            def __next__(self) -> str:
                if self.__count < self._num_fields - 1:
                    to_return = self.fields[self.__count].get_padded_text()
                elif self.__count == self._num_fields - 1:
                    to_return = self.fields[self.__count].get_text()
                else:
                    raise StopIteration
                self.__count += 1
                return to_return

        return FieldIter(self.__fields)

    def get_node(self, row: int):
        """
        :param row: the row the returned NestedList starts at relative to this node
        :returns: the NestedList that starts at row. None if out of bounds
        """
        if row == 0:
            return self
        row -= 1
        child_count = self.__child.count()
        if row < child_count:
            return self.__child.get_node(row)
        row -= child_count
        sibling_count = self.__sibling.count()
        if row < sibling_count:
            return self.__sibling.get_node(row)
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
    Functions called by KeyCommand
    """

    def delete_first_child(self):
        """deletes branch of nested list starting at first child"""
        self._set_child(self.__child.__sibling)

    def delete_next_sibling(self):
        """delete branch of nested list starting at next sibling"""
        self._set_sibling(self.__sibling.__sibling)

    def insert(self, x_coord, insertion: str):
        """inserts a string into a pre-existing field"""
        field = self._get_field(x_coord)
        text: str = field.get_text()
        index = self.get_rel_field_index(x_coord)
        new_text = text[0:index] + insertion + text[index:len(text)]
        field.replace_text(new_text)

    def delete_char_at(self, x_coord: int):
        field = self._get_field(x_coord)
        text: str = field.get_text()
        index = self.get_rel_field_index(x_coord)
        new_text = text[0:index] + text[index + 1:len(text)]
        field.replace_text(new_text)

    def split_field(self, x_coord: int):
        field_index = self._get_field_index(x_coord)
        field_to_split = self.__fields[field_index]
        split_index = self.get_rel_field_index(x_coord)
        left_text = field_to_split[0:split_index]
        right_text = field_to_split[split_index:]
        self.__fields[field_index].replace_text(left_text)
        self.insert_field(right_text, field_index + 1)

    def split(self, x_coord: int):
        """
        Create a new node as a sibling with all fields right of the x_coord, inclusive
        These fields are removed from this node
        :param x_coord:
        """
        field_index = self._get_field_index(x_coord)
        split_fields = self.__fields[field_index:]
        texts: List[str] = []
        for field in split_fields:
            texts.append(field.get_text())
        del self.__fields[field_index:]
        self.new_sibling(texts)
        self._give_child(self.__sibling)

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

    def combine_fields(self, x_coord: int, direction: LateralDirection):
        field_index = self._get_field_index(x_coord)
        current_field = self.__fields[field_index]
        other_field = self.__fields[field_index + direction]
        if direction == LateralDirection.LEFT:
            left_field = other_field
            right_field = current_field
            right_field_index = field_index
        else:
            left_field = current_field
            right_field = other_field
            right_field_index = field_index + direction
        text_left = left_field.get_text()
        text_right = right_field.get_text()
        left_field.replace_text(text_left + text_right)
        self.remove_field(right_field_index)

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

    def _set_level(self, new_level: int):
        pass

    def _decrement_level(self):
        pass

    def _update_columns(self, new_columns: List[_Column] = None):
        pass

    def _get_columns(self) -> List[_Column]:
        return []

    def _set_sibling(self, next_sibling):
        pass

    def _set_child(self, first_child):
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
