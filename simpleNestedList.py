from typing import List
from row import Row
from column import Column


class SimpleNestedList(object):
    """
    Encapsulates the column and level data
    """

    def __init__(self, fields: List[str] = None, columns: List[Column] = None):
        """
        :param fields:
        :param columns: Should only be used privately by SimpleNestedList.
            Unfortunately, python does not support private constructors.
        """
        if fields is None:
            fields = []
        if columns is None:
            columns = []
        self.__columns = columns
        self.__row = Row(columns, fields)
        # links to neighboring nested list nodes
        self.__child = self.null
        self.__sibling = self.null
        # are the children hidden
        self.__collapsed = False
        # indentation level
        self.__level = 0

    @staticmethod
    def _new_nested_list(level: int, columns: List[Column], fields: List[str] = None,
                         next_sibling=None, first_child=None):
        """
        :return: new NestedList
        """
        if fields is None:
            fields = []
        node = SimpleNestedList(fields)
        node.__columns = columns
        for index in range(len(columns), len(fields)):
            node.__columns.append(_Column())
        for index, text in enumerate(fields):
            node.__fields.append(_Field(text, node.__columns[index], tab))

        node.__level = level
        if next_sibling is not None:
            node.__sibling = next_sibling
        if first_child is not None:
            node.__child = first_child
        return node

    @property
    def null(self):
        return _NullRow.getInstance()

    @property
    def _columns(self):
        """
        For polymorphism with _NullRow
        """
        # TODO make an inner class node and use decorator getters and setters
        return self.__columns

    @_columns.deleter
    def _columns(self):
        # called when node is deleted
        # TODO
        for field in self.__fields:
            del field.column

    @property
    def level(self):
        return self.__level

    @property
    def sibling(self):
        return self.__sibling

    @sibling.setter
    def sibling(self, next_sibling):
        """
        attach a pre-existing nestedList row and all its siblings and children
        To insert a sibling row without any descendents, call self.insert_sibling
        :param next_sibling:
        :return:
        """
        # TODO remove other places where columns and levels were updated manually
        self.__sibling = next_sibling
        next_sibling.__update_columns(new_columns=self._get_columns())
        next_sibling._set_level(self.__level)

    @sibling.deleter
    def sibling(self):
        """
        Deletes the sibling row only, not its children or siblings
        Removes row references and
        """
        # TODO repair links and remove fields from columns
        del self.sibling.columns
        self.append_child(self.sibling.child)
        self.sibling = self.sibling.sibling

    def insert_sibling(self, texts: List[str] = None):
        if texts is None:
            texts = []
        self.__sibling = self._new_nested_list(tab=self.__tab, columns=self._get_columns(), fields=texts,
                                               level=self.__level, next_sibling=self.__sibling)
        return self.__sibling

    def delete_sibling_list(self):
        """
        Delete the nested list starting at sibling
        """
        # TODO

    @property
    def child(self):
        return self.__child

    @child.setter
    def child(self, new_child):
        """
        attach a pre-existing nestedList row and all its siblings and children
        To insert a child row without any descendents, call self.insert_child or self.append_child
        :param new_child:
        :return:
        """
        old_child_columns: List[_Column] = self.__child._get_columns()
        self.__child = new_child
        new_child.__update_columns(new_columns=old_child_columns)
        new_child._set_level(self.__level + 1)

    @child.deleter
    def child(self):
        """
        Deletes the child row only, not its children or siblings
        """
        # TODO repair links and remove fields from columns
        del self.child.columns
        self.__child = self.child.sibling

    def delete_child_list(self):
        """
        Deletes the nested list starting at child
        """
        # TODO

    def append_child(self, texts: List[str] = None):
        """
        Adds new child as the last child under this
        :param new_child: The NestedList to append
        """
        if isinstance(self.__child, _NullRow):
            self.insert_child(texts)
        else:
            last_child = self.__child.get_last_sibling()
            last_child.insert_sibling(texts)

    def insert_child(self, texts: List[str] = None):
        if texts is None:
            texts = []
        child_cols = self.__child._get_columns()
        self.__child = self._new_nested_list(tab=self.__tab, columns=child_cols, fields=texts,
                                             level=self.__level + 1, next_sibling=self.__child)
            return self.__child

    def _set_level(self, new_level: int):
        self.__level = new_level
        self.__child._set_level(new_level)
        self.__sibling._set_level(new_level)

    def _columns(self):
        # TODO make an inner class node and use decorator getters and setters
        return self.__columns

    def insert_field(index):
        assert len(self.__columns) >= len(self.__fields)
        new_field = _Field(text=text, column=self.__columns[index], tab=self.__tab)
        self.__fields.insert(index, new_field)
        self.__update_columns(index+1)
    # TODO

    def delete_field(self, index):
        del self.__fields(index)

    def remove_field(self, index):
        del self.__fields[index]
        self.__update_columns(index)

    def replace_field(index):
        # TODO


class _NullRow(Row):
    # TODO
    @property
    def _columns(self):
        """
        For creating a new array of columns when the new node has no sibling
        """
        return []

    @property
    def level(self):
        raise Exception("Not allowed for NullRow")

    @property
    def child(self):
        return self

    @property
    def sibling(self):
        return self


class _Column(object):
    """
    Unordered collection of data communicated between fields of the same column in different rows
    of the same level
    """

    def __init__(self):
        """
        Each counter in this list is the collection of sizes of each cell for a column
        """
        self.__field_widths = Counter()

    def add_field(self, width):
        self.__field_widths[width] += 1

    def remove_field(self, width):
        self.__field_widths[width] -= 1

    def get_width(self) -> int:
        return max(self.__field_widths.elements())


class _Field(object):
    def __init__(self, text: str, column: _Column, tab: str):
        self.__tab = tab
        self.__tab_len = len(tab)
        self.__col = column
        self.__text = text
        column.add_field(len(text))

    def __eq__(self, other):
        if not isinstance(other, _Field):
            return False
        return self.__text == other.__text

    def __len__(self) -> int:
        """
        :return: size of field including padding
        """
        col_width = self.__col.get_width()
        return col_width + self.__tab_len

    def __getitem__(self, key):
        return self.__text[key]

    def __del__(self):
        self.__col.remove_field(len(self.__text))

    #@column.deleter
    #def column(self):
    #    self.__col.remove_field(len(self.__text))

    def get_text(self) -> str:
        return self.__text

    def get_padded_text(self) -> str:
        return self.__text + self.__tab + ' ' * (self.get_padding_len() - self.__tab_len)

    def get_text_len(self) -> int:
        return len(self.__text)

    def get_padding_len(self) -> int:
        return len(self) - self.get_text_len()

    #def replace_text(self, new_text: str):
    #    self.__col.remove_field((len(self.__text)))
    #    self.__col.add_field(len(new_text))
    #    self.__text = new_text

    #def replace_column(self, col: _Column):
    #    self.__col.remove_field(len(self.__text))
    #    self.__col = col
    #    self.__col.add_field(len(self.__text))

