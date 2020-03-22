from column import Column
from typing import List, Callable


class Row(object):
    """
    Holds a list of strings, each attached to a column. These columns are shared with other rows.
    """

    __tab_len = 4

    def __detach_columns(self, index: int):
        """
        remove fields from respective columns from index to the end of self.__fields
        :param index: starting field to detach from its column
        """
        for index in range(index, len(self.__fields)):
            field_len = len(self.__fields[index])
            self.__columns[index].remove_field(field_len)

    def __attach_columns(self, index: int):
        """
        add new field lengths to each column from index to the end of self.__fields
        :param index: starting field to attach to its column
        """
        for index in range(index, len(self.__fields)):
            field_len = len(self.__fields[index])
            self.__columns[index].add_field(field_len)

    # Public methods

    def __init__(self, columns: List[Column], fields: List[str] = None):
        self.__fields = []
        if fields is None:
            fields = []
        self.__columns = columns
        for field in fields:
            self.append(field)

    def __del__(self):
        """
        detach all columns from self
        """
        for i in range(len(self)):
            self.__detach_columns(i)

    def delete(self, index):
        """
        Delete the field at index and update related column
        """
        self.__detach_columns(index)
        del self.__fields[index]
        self.__attach_columns(index)

    def insert(self, index: int, text: str):
        self.__detach_columns(index)
        # Insert new field
        self.__fields.insert(index, text)
        # Add new column if necessary
        if len(self.__fields) > len(self.__columns):
            self.__columns.append(Column())
        self.__attach_columns(index)

    def replace(self, index: int, text: str):
        """
        Replace an existing field with new text
        """
        self.__columns[index].remove_field(len(self.__fields[index]))
        self.__fields[index] = text
        self.__columns[index].add_field(len(self.__fields[index]))

    def append(self, text: str):
        self.insert(len(self), text)

    """
    Getters
    """

    def __len__(self):
        """
        :return: how many fields are in this row
        """
        return len(self.__fields)

    def width(self) -> int:
        """
        :return: Sum of all characters in this row, including padding
        Not including indentation
        """
        to_return = 0
        for field in self:
            to_return += len(field)
        return to_return

    def padded_field_len(self, index: int):
        return self.__columns[index].width + self.__tab_len

    def field(self, index: int):
        """
        Return the unpadded text of the field at index
        """
        return self.__fields[index]

    def padded_field(self, index: int):
        return self.__fields[index] + ' ' * self.padding_len(index)

    def padding_len(self, index: int):
        return self.padded_field_len(index) - self.text_len(index)

    def text_len(self, index: int):
        return len(self.__fields[index])

    @property
    def fields(self) -> List[str]:
        return self.__fields

    def __iter__(self):
        class RowIter(object):
            def __init__(self, row):
                self.__index = 0
                self.__row = row

            def __next__(self):
                if self.__index < len(self.__row) - 1:
                    # pad all but last field
                    to_return = self.__row.padded_field(self.__index)
                elif self.__index == len(self.__row) - 1:
                    # no padding on last field
                    to_return = self.__row.field(self.__index)
                else:
                    raise StopIteration
                self.__index += 1
                return to_return

        return RowIter(self)

    def __eq__(self, other):
        if not isinstance(other, Row):
            return False
        if len(self) != len(other):
            return False
        for index in range(len(self)):
            if self.padded_field(index) != other.padded_field(index):
                return False
        return True
