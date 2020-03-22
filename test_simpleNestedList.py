#!/usr/bin/python3
import unittest
from simpleNestedList import SimpleNestedList

class TestSimpleNestedList(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
