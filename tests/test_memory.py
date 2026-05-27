import unittest
from src.db.backend.memory import StudentTable
from src.db.backend.errors import (
    InvalidAgeError,
    DuplicateIDError,
    RecordNotFoundError,
    InvalidNameError,
    InvalidSexError
)

class TestStudentTable(unittest.TestCase):
    def setUp(self):
        self.table = StudentTable()
        self.test_records = [
            (1, "John", "Doe", 20, "М"),
            (2, "Jane", "Smith", 22, "Ж"),
            (3, "Alice", "Johnson", 19, "Ж"),
            (4, "Bob", "Brown", 21, "М"),
            (5, "Charlie", "Davis", 18, "М"),
        ]
        for record in self.test_records:
            self.table.create_record(*record)

    def test_create_record_success(self):
        new_record = self.table.create_record(6, "Test", "User", 25, "М")
        self.assertEqual(new_record[0], 6)
        self.assertEqual(self.table.get_record_count(), 6)

    def test_create_record_invalid_age_negative(self):
        with self.assertRaises(InvalidAgeError):
            self.table.create_record(6, "Test", "User", -5, "М")

    def test_create_record_invalid_age_too_high(self):
        with self.assertRaises(InvalidAgeError):
            self.table.create_record(6, "Test", "User", 200, "М")

    def test_create_record_duplicate_id(self):
        with self.assertRaises(DuplicateIDError):
            self.table.create_record(1, "Test", "User", 25, "М")

    def test_create_record_empty_first_name(self):
        with self.assertRaises(InvalidNameError):
            self.table.create_record(6, "   ", "User", 25, "М")

    def test_create_record_empty_second_name(self):
        with self.assertRaises(InvalidNameError):
            self.table.create_record(6, "Test", "   ", 25, "М")

    def test_create_record_invalid_sex(self):
        with self.assertRaises(InvalidSexError):
            self.table.create_record(6, "Test", "User", 25, "X")

    def test_select_record_no_filters(self):
        records = self.table.select_record()
        self.assertEqual(len(records), 5)

    def test_select_record_by_id(self):
        records = self.table.select_record(student_id=1)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][0], 1)

    def test_select_record_by_first_name(self):
        records = self.table.select_record(first_name="jane")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][1], "Jane")

    def test_select_record_by_age(self):
        records = self.table.select_record(age=20)
        self.assertEqual(len(records), 1)

    def test_select_record_by_sex(self):
        records = self.table.select_record(sex="М")
        self.assertEqual(len(records), 3)

    def test_update_record_success(self):
        updated = self.table.update_record(1, first_name="Jonathan", age=21)
        self.assertEqual(updated[1], "Jonathan")
        self.assertEqual(updated[3], 21)

    def test_update_record_not_found(self):
        with self.assertRaises(RecordNotFoundError):
            self.table.update_record(999, first_name="Test")

    def test_delete_record_by_id(self):
        deleted = self.table.delete_record(student_id=1)
        self.assertEqual(deleted, 1)
        self.assertEqual(self.table.get_record_count(), 4)

    def test_delete_record_no_filters(self):
        with self.assertRaises(ValueError):
            self.table.delete_record()

    def test_delete_record_not_found(self):
        deleted = self.table.delete_record(student_id=999)
        self.assertEqual(deleted, 0)

    def test_get_all_records(self):
        records = self.table.get_all_records()
        self.assertEqual(len(records), 5)

    def test_get_record_count(self):
        count = self.table.get_record_count()
        self.assertEqual(count, 5)

if __name__ == '__main__':
    unittest.main()
