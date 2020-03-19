#!/usr/bin/python3
import unittest
from row import Row


class TestRow(unittest.TestCase):

    def test_eq(self):
        row = Row(columns=[], fields=["one", "two", "three"])
        self.assertEqual(row, row)
        row2 = Row(columns=[], fields=["one", "two", "three"])
        self.assertEqual(row, row2)
        columns = []
        row3 = Row(columns, fields=["one", "two", "three"])
        # causes row3 to have an extra column, but shouldn't affect equality
        other = Row(columns, fields=["one", "two", "three", ""])
        self.assertEqual(row, row3)
        row_diff = Row(columns=[], fields=["one", "two", "threeE"])
        self.assertNotEqual(row, row_diff)
        row_diff2 = Row(columns=[], fields=["one", "two"])
        self.assertNotEqual(row, row_diff2)
        diff_columns = []
        row_diff3 = Row(diff_columns, ["one", "two", "three"])
        # creates a different column width in the first column of row_diff3
        row_other = Row(diff_columns, ["1234"])
        self.assertNotEqual(row, row_diff3)

    def test_insert(self):
        actual = Row(columns=[], fields=["one", "two", "three"])
        target = Row(columns=[], fields=["one", "two", "three", "four"])
        actual.append("four")
        self.assertEqual(actual, target)
        actual = Row(columns=[], fields=[])
        target = Row(columns=[], fields=["one"])
        actual.insert(0, "one")
        self.assertEqual(actual, target)
        actual = Row(columns=[], fields=["one", "three"])
        target = Row(columns=[], fields=["one", "two", "three"])
        actual.insert(1, "two")
        self.assertEqual(actual, target)

    def test_remove(self):
        actual = Row(columns=[], fields=["one", "two", "three", "four"])
        target = Row(columns=[], fields=["one", "two", "three"])
        actual.delete(3)
        self.assertEqual(actual, target)
        target = Row(columns=[], fields=["one", "three"])
        actual.delete(1)
        self.assertEqual(actual, target)
        target = Row(columns=[], fields=["three"])
        actual.delete(0)
        self.assertEqual(actual, target)

    def test_replace(self):
        actual = Row(columns=[], fields=["one", "two", "three"])
        target = Row(columns=[], fields=["one", "two", "3"])
        actual.replace(2, "3")
        self.assertEqual(actual, target)
        target = Row(columns=[], fields=["1", "two", "3"])
        actual.replace(0, "1")
        self.assertEqual(actual, target)

    def test_iter(self):
        actual = Row(columns=[], fields=["one", "two", "three"])
        target = "one    two    three"
        result = ''
        for field in actual:
            result += field
        self.assertEqual(result, target)

    def test_iter_complex(self):
        columns = []
        actual = Row(columns, fields=["one", "two", "three"])
        Row(columns, fields=["0123", "123", "0123456"])
        target = "one     two    three"
        result = ''
        for field in actual:
            result += field
        self.assertEqual(result, target)

    def test_getters(self):
        columns = []
        row = Row(columns, fields=["one", "two", "three"])
        Row(columns, fields=["0123", "123", "0123456"])
        self.assertEqual(len(row), 3)
        self.assertEqual(row.field(2), "three")
        self.assertEqual(row.text_len(0), 3)
        self.assertEqual(row.padded_field_len(2), 11)
        self.assertEqual(row.padding_len(2), 6)
        self.assertEqual(row.padded_field(0), "one     ")
