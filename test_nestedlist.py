#!/usr/bin/python3
import unittest
from nestedlist import NestedList, NullNestedList
from typing import List


class TestNestedList(unittest.TestCase):

    def test_init(self):
        root = NestedList()

    def test_get_count(self):
        root = NestedList()
        self.assertEqual(root.count(), 1)
        sibling = root.insert_sibling()
        self.assertEqual(root.count(), 2)
        child = sibling.insert_child()
        self.assertEqual(sibling.count(), 2)
        self.assertEqual(root.count(), 3)
        grandchild = child.insert_child()
        self.assertEqual(root.count(), 4)
        grandchild2 = grandchild.insert_sibling()
        self.assertEqual(root.count(), 5)
        grandchild.insert_sibling()
        self.assertEqual(root.count(), 6)
        child.insert_sibling()
        self.assertEqual(root.count(), 7)

    def test_new_node(self):
        root = NestedList()
        child = root.insert_child()
        grandchild = child.insert_child()
        child2 = child.insert_sibling()
        self.assertIs(root.child, child)
        self.assertIs(child.sibling, child2)
        self.assertIs(root.child.child, grandchild)

    def test_get_node(self):
        root = NestedList()
        child = root.insert_child()
        grandchild = child.insert_child()
        child2 = child.insert_sibling()
        """
        root
            child
                grandchild
            child2
        """
        self.assertIs(root.get_node(0), root)
        self.assertIs(root.get_node(1), child)
        self.assertIs(root.get_node(2), grandchild)
        self.assertIs(root.get_node(3), child2)

        grandchild2 = grandchild.insert_sibling()
        child3 = child2.insert_sibling()
        greatgrandchild = grandchild.insert_child()
        """
        root
            child
                grandchild
                    greatgrandchild
                grandchild2
            child2
            child3
        """
        self.assertIs(root.get_node(0), root)
        self.assertIs(root.get_node(1), child)
        self.assertIs(root.get_node(2), grandchild)
        self.assertIs(root.get_node(3), greatgrandchild)
        self.assertIs(root.get_node(4), grandchild2)
        self.assertIs(root.get_node(5), child2)
        self.assertIs(root.get_node(6), child3)

    def __test_iter_helper(self, root: NestedList,  targets: List[NestedList]):
        for index, actual in enumerate(root):
            self.assertIs(actual, targets[index])

    def test_iter(self):
        root = NestedList(self.tab)
        # breakpoint()
        self.__test_iter_helper(root, [root])
        child = root.insert_child()
        self.__test_iter_helper(root, [root, child])
        child2 = child.insert_sibling()
        self.__test_iter_helper(root, [root, child, child2])
        grandchild = child2.insert_child()
        self.__test_iter_helper(root, [root, child, child2, grandchild])
        child3 = child2.insert_sibling()
        self.__test_iter_helper(root, [root, child, child2, grandchild, child3])
        greatgrandchild = grandchild.insert_child()
        self.__test_iter_helper(root, [root, child, child2, grandchild, greatgrandchild, child3])
        greatgreatgrandchild = greatgrandchild.insert_child()
        self.__test_iter_helper(root, [root, child, child2, grandchild, greatgrandchild, greatgreatgrandchild, child3])
        sibling2 = root.insert_sibling()
        sibling = root.insert_sibling()
        self.__test_iter_helper(root, [root, child, child2, grandchild, greatgrandchild, greatgreatgrandchild, child3, sibling, sibling2])

    def test_eq(self):
        root = NestedList(tab=self.tab, fields=["01234"])
        child = root.insert_child(texts=["012", "0", "0"])
        child.insert_child(["012"])
        child.insert_sibling(["0", "0", "0123", ""])

        root_copy = NestedList(tab=self.tab, fields=["01234"])
        child_copy = root_copy.insert_child(texts=["012", "0", "0"])
        child_copy.insert_child(["012"])
        child_copy.insert_sibling(["0", "0", "0123", ""])

        self.assertEqual(root, root_copy)

        root_dif = NestedList(tab=self.tab, fields=["01234"])
        child_dif = root_dif.insert_child(texts=["012", "0", "0"])
        child_dif.insert_child(["012"])
        child_dif.insert_sibling(["0", "0", "0123", "9"])

        self.assertNotEqual(root, root_dif)

    def test_unindent(self):
        root = NestedList(tab=self.tab, fields=["root"])
        child = root.insert_child(texts=["child"])
        child2 = child.insert_sibling(["child2"])
        grandchild = child2.insert_child(["grandchild"])
        child3 = child2.insert_sibling(["child3"])
        child3.insert_child(["grandchild2"])
        """
        root
            child
            child2
                grandchild
            child3
                grandchild2
        """
        # Indent child
        target_root = NestedList(tab=self.tab, fields=["root"])
        target_child = target_root.insert_sibling(texts=["child"])
        target_child2 = target_child.insert_child(["child2"])
        target_child2.insert_child(["grandchild"])
        target_child3 = target_child2.insert_sibling(["child3"])
        target_child3.insert_child(["grandchild2"])
        """
        root
        child
            child2
                grandchild
            child3
                grandchild2
        """
        child.unindent(parent=root, prev_sibling=NullNestedList.get_instance())
        self.assertEqual(root, target_root)

        # Indent child 2
        target_root = NestedList(tab=self.tab, fields=["root"])
        target_child = target_root.insert_sibling(texts=["child"])
        target_child2 = target_child.insert_sibling(["child2"])
        target_grandchild = target_child2.insert_child(["grandchild"])
        target_child3 = target_grandchild.insert_sibling(["child3"])
        target_child3.insert_child(["grandchild2"])
        """
        root
        child
        child2
            grandchild
            child3
                grandchild2
        """
        child2.unindent(parent=child, prev_sibling=NullNestedList.get_instance())
        self.assertEqual(root, target_root)

        # Indent child3
        target_root = NestedList(tab=self.tab, fields=["root"])
        target_child = target_root.insert_sibling(texts=["child"])
        target_child2 = target_child.insert_sibling(["child2"])
        target_child2.insert_child(["grandchild"])
        target_child3 = target_child2.insert_sibling(["child3"])
        target_child3.insert_child(["grandchild2"])
        """
        root
        child
        child2
            grandchild
        child3
            grandchild2
        """
        child3.unindent(parent=child2, prev_sibling=grandchild)
        self.assertEqual(root, target_root)


if __name__ == '__main__':
    unittest.main()
