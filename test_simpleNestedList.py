#!/usr/bin/python3
import unittest
from simpleNestedList import SimpleNestedList


class TestSimpleNestedList(unittest.TestCase):
    """
    Currently not usable because SimpleNestedList is an abstract class, subclassed by NestedList
    """

    def test_eq(self):
        root = SimpleNestedList(["root"])
        self.assertEqual(root, root)
        target = SimpleNestedList(["root"])
        self.assertEqual(root, target)
        diff = SimpleNestedList(["rooA"])
        self.assertNotEqual(root, diff)
        diff = SimpleNestedList(["root"])
        diff.insert_child()
        self.assertNotEqual(root, diff)
        diff = SimpleNestedList(["root"])
        diff.insert_sibling()
        self.assertNotEqual(root, diff)

    def test_columns(self):
        one = SimpleNestedList(["123", "1"])
        self.__test_columns_helper(one, "123    1")
        two = one.insert_sibling(["12345"])
        self.__test_columns_helper(one, "123      1")
        two.insert_field(0, "1234")
        self.__test_columns_helper(one, "123     1")

    def __test_columns_helper(self, row: SimpleNestedList, target: str):
        actual = ""
        for field in one.row_iter:
            actual += field
        self.assertEqual(actual, target)




if __name__ == '__main__':
    unittest.main()
