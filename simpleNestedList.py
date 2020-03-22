from typing import List
from row import Row
from column import Column


class SimpleNestedList(object):
    """
    Encapsulates the column and level data
    """

    __indent_len = 4

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
        # indentation level
        self.__level = 0

    @classmethod
    def _new_nested_list(cls, level: int, columns: List[Column], fields: List[str] = None,
                         next_sibling=None, first_child=None):
        """
        :return: new NestedList
        """
        if fields is None:
            fields = []
        node = cls.__init__(fields, columns)
        node.__level = level
        if next_sibling is not None:
            node.__sibling = next_sibling
        if first_child is not None:
            node.__child = first_child
        return node

    def __del__(self):
        del self._columns

    @property
    def null(self):
        raise Exception("Implemented by subclass")
        # return _NullSimpleNestedList.getInstance()

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
        self.__row.delete()

    @property
    def level(self):
        return self.__level

    def _set_level(self, new_level: int):
        self.__level = new_level
        self.__child._set_level(new_level)
        self.__sibling._set_level(new_level)

    @property
    def sibling(self):
        return self.__sibling

    @sibling.deleter
    def sibling(self):
        """
        Deletes the sibling row only, not its children or siblings
        Removes row references and
        """
        # TODO repair links and remove fields from columns
        del self.sibling.columns
        self.append_child(self.sibling.child)
        self.__sibling = self.sibling.sibling

    def insert_sibling(self, texts: List[str] = None):
        if texts is None:
            texts = []
        self.__sibling = self._new_nested_list(columns=self._columns, fields=texts,
                                               level=self.__level, next_sibling=self.__sibling)
        return self.__sibling

    @property
    def child(self):
        return self.__child

    @child.deleter
    def child(self):
        """
        Deletes the child row only, not its children or siblings
        """
        # TODO repair links and remove fields from columns
        del self.child.columns
        self.__child = self.child.sibling

    def append_child(self, texts: List[str] = None):
        """
        Adds new child as the last child under this
        :param new_child: The NestedList to append
        """
        if self.__child is self.null:
            self.insert_child(texts)
        else:
            last_child = self.__child.get_last_sibling()
            last_child.insert_sibling(texts)

    def insert_child(self, texts: List[str] = None):
        if texts is None:
            texts = []
        child_cols = self.__child._columns
        self.__child = self._new_nested_list(columns=child_cols, fields=texts,
                                             level=self.__level + 1, next_sibling=self.__child)
        return self.__child

    @property
    def indent_padding(self) -> str:
        return (' ' * self.__indent_len) * self.level

    """
    Row operations
    """

    @property
    def fields(self) -> List[str]:
        return self.__row.fields

    @property
    def num_fields(self) -> int:
        return len(self.__row)

    @property
    def row_iter(self):
        return iter(self.__row)

    @property
    def width(self) -> int:
        """
        :return: num characters in string representation of fields including indentation and separation
        """
        return self.__row.width() + len(self.indent_padding)

    def insert_field(self, index: int, text: str):
        self.__row.insert(index, text)

    def delete_field(self, index):
        self.__row.delete(index)

    def replace_field(self, index: int, replacement: str):
        self.__row.replace(index, replacement)

    def _get_field(self, index: int) -> str:
        return self.__row.field(index)


