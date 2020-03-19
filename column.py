from collections import Counter


class Column(object):
        """
        Data communicated between sibling Rows
        """

        def __init__(self):
            """
            Each counter in this list is the collection of sizes of each cell for a column
            """
            self.__field_widths = Counter()

        def add_field(self, width: int):
            self.__field_widths[width] += 1

        def remove_field(self, width: int):
            self.__field_widths[width] -= 1

        @property
        def width(self) -> int:
            """
            :return: max width of all fields
            """
            return max(self.__field_widths.elements())

