import unittest
from model import Model
from testView import TestView
from nestedlist import NestedList
from directions import LateralDirection


class MyTestCase(unittest.TestCase):

    # Getters

    def test_get_node(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = one.insert_sibling(["three"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model._Model__get_node(), one)
        model._Model__cursor_y = 1
        self.assertEqual(model._Model__get_node(), two)
        model._Model__cursor_y = 2
        self.assertEqual(model._Model__get_node(), three)
        four = two.insert_child(["four"])
        """
        one
            two
                four
        three
        """
        model._Model__cursor_y = 2
        self.assertEqual(model._Model__get_node(), four)
        five = one.insert_sibling(["five"])
        """
        one
            two
                four
        five
        three
        """
        model._Model__cursor_y = 3
        self.assertEqual(model._Model__get_node(), five)

    def test_get_level(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = one.insert_sibling(["three"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        self.assertEqual(model.get_level(), 0)
        model._Model__cursor_y = 1
        self.assertEqual(model.get_level(), 1)
        model._Model__cursor_y = 2
        self.assertEqual(model.get_level(), 0)

    def test_get_previous_sibling(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = two.insert_sibling(["three"])
        four = one.insert_sibling(["four"])
        """
        one
            two
            three
        four
        """
        model = Model(TestView([]), one)
        model._Model__cursor_y = 3
        self.assertIs(one, model.get_previous_sibling())
        model._Model__cursor_y = 2
        self.assertIs(two, model.get_previous_sibling())

    def test_get_parent(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = two.insert_sibling(["three"])
        four = one.insert_sibling(["four"])
        five = four.insert_child(["five"])
        """
        one
            two
            three
        four
            five
        """
        model = Model(TestView([]), one)
        model._Model__cursor_y = 2
        self.assertIs(one, model.get_parent())
        model._Model__cursor_y = 4
        self.assertIs(four, model.get_parent())

    def test_get_column_width(self):
        one = NestedList(["one", "two.", "three"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_column_width(), 7)
        model._Model__cursor_x = 2
        self.assertEqual(model.get_column_width(), 7)
        model._Model__cursor_x = 6
        self.assertEqual(model.get_column_width(), 7)
        model._Model__cursor_x = 7
        self.assertEqual(model.get_column_width(), 8)
        model._Model__cursor_x = 11
        self.assertEqual(model.get_column_width(), 8)
        model._Model__cursor_x = 15
        self.assertEqual(model.get_column_width(), 9)
        model._Model__cursor_x = 20
        self.assertEqual(model.get_column_width(), 9)

    def test_get_neighbor_column_width(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        one = NestedList(["one", "two.", "three"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_neighbor_column_width(right), 8)
        model._Model__cursor_x = 2
        self.assertEqual(model.get_neighbor_column_width(right), 8)
        model._Model__cursor_x = 6
        self.assertEqual(model.get_neighbor_column_width(right), 8)
        model._Model__cursor_x = 7
        self.assertEqual(model.get_neighbor_column_width(right), 9)
        self.assertEqual(model.get_neighbor_column_width(left), 7)
        model._Model__cursor_x = 11
        self.assertEqual(model.get_neighbor_column_width(right), 9)
        self.assertEqual(model.get_neighbor_column_width(left), 7)
        model._Model__cursor_x = 15
        self.assertEqual(model.get_neighbor_column_width(left), 8)
        model._Model__cursor_x = 20
        self.assertEqual(model.get_neighbor_column_width(left), 8)

    def test_get_neighbor_field(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        fields = ["one", "two.", "three"]
        one = NestedList(fields)
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_neighbor_field(right), fields[1])
        model._Model__cursor_x = 2
        self.assertEqual(model.get_neighbor_field(right), fields[1])
        model._Model__cursor_x = 6
        self.assertEqual(model.get_neighbor_field(right), fields[1])
        model._Model__cursor_x = 7
        self.assertEqual(model.get_neighbor_field(right), fields[2])
        self.assertEqual(model.get_neighbor_field(left), fields[0])
        model._Model__cursor_x = 11
        self.assertEqual(model.get_neighbor_field(right), fields[2])
        self.assertEqual(model.get_neighbor_field(left), fields[0])
        model._Model__cursor_x = 15
        self.assertEqual(model.get_neighbor_field(left), fields[1])
        model._Model__cursor_x = 20
        self.assertEqual(model.get_neighbor_field(left), fields[1])

    def test_get_padding_len(self):
        one = NestedList(["one", "two.", "three"])
        one.insert_sibling(["one", "two.5", "three56"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_padding_len(), 4)
        model._Model__cursor_x = 2
        self.assertEqual(model.get_padding_len(), 4)
        model._Model__cursor_x = 6
        self.assertEqual(model.get_padding_len(), 4)
        model._Model__cursor_x = 7
        self.assertEqual(model.get_padding_len(), 5)
        model._Model__cursor_x = 11
        self.assertEqual(model.get_padding_len(), 5)
        model._Model__cursor_x = 16
        self.assertEqual(model.get_padding_len(), 6)
        model._Model__cursor_x = 21
        self.assertEqual(model.get_padding_len(), 6)

    def test_get_neighbor_padding_len(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        one = NestedList(["one", "two.", "three"])
        one.insert_sibling(["one", "two.5", "three56"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_neighbor_padding_len(right), 5)
        model._Model__cursor_x = 2
        self.assertEqual(model.get_neighbor_padding_len(right), 5)
        model._Model__cursor_x = 6
        self.assertEqual(model.get_neighbor_padding_len(right), 5)
        model._Model__cursor_x = 7
        self.assertEqual(model.get_neighbor_padding_len(right), 6)
        self.assertEqual(model.get_neighbor_padding_len(left), 4)
        model._Model__cursor_x = 11
        self.assertEqual(model.get_neighbor_padding_len(right), 6)
        self.assertEqual(model.get_neighbor_padding_len(left), 4)
        model._Model__cursor_x = 16
        self.assertEqual(model.get_neighbor_padding_len(left), 5)
        model._Model__cursor_x = 21
        self.assertEqual(model.get_neighbor_padding_len(left), 5)

    # Location Getters

    def test_is_first_child(self):
        root = NestedList(["root"])
        child = root.insert_child(["child"])
        child2 = child.insert_sibling(["child2"])
        grandchild = child2.insert_child(["grandchild"])
        grandchild2 = grandchild.insert_sibling(["grandchild2"])
        child3 = child2.insert_sibling(["child3"])
        """
        root
            child
            child2
                grandchild
                grandchild2
            child3
        """
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        self.assertFalse(model.is_first_child())
        model._Model__cursor_y = 1
        self.assertTrue(model.is_first_child())
        model._Model__cursor_y = 2
        self.assertFalse(model.is_first_child())
        model._Model__cursor_y = 3
        self.assertTrue(model.is_first_child())
        model._Model__cursor_y = 4
        self.assertFalse(model.is_first_child())
        model._Model__cursor_y = 5
        self.assertFalse(model.is_first_child())

    def test_at_root(self):
        root = NestedList(["root"])
        child = root.insert_child(["child"])
        child2 = child.insert_sibling(["child2"])
        grandchild = child2.insert_child(["grandchild"])
        grandchild2 = grandchild.insert_sibling(["grandchild2"])
        child3 = child2.insert_sibling(["child3"])
        """
        root
            child
            child2
                grandchild
                grandchild2
            child3
        """
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        self.assertTrue(model.at_root())
        model._Model__cursor_y = 1
        self.assertFalse(model.at_root())
        model._Model__cursor_y = 2
        self.assertFalse(model.at_root())
        model._Model__cursor_y = 3
        self.assertFalse(model.at_root())
        model._Model__cursor_y = 4
        self.assertFalse(model.at_root())
        model._Model__cursor_y = 5
        self.assertFalse(model.at_root())

    def test_at_line_start(self):
        pass

    def test_at_line_end(self):
        pass

    def test_at_field_start(self):
        pass

    def test_at_field_end(self):
        pass

    # Actions

    def test_move(self):
        pass

    def test_move_end(self):
        pass

    def test_move_field_end(self):
        pass

    def test_delete(self):
        pass

    def test_insert(self):
        pass

    def test_split_field(self):
        pass

    def test_combine_field(self):
        pass

    def test_indent_current_node(self):
        pass

    def test_unindent_current_node(self):
        pass

    def test_combine_nodes(self):
        pass




if __name__ == '__main__':
    unittest.main()
