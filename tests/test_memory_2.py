import unittest
from src.db.backend.memory import StudentTable
from src.db.backend.errors import InvalidAgeError, DuplicateIDError, RecordNotFoundError, InvalidNameError, \
    InvalidSexError


class TestMemoryExtra(unittest.TestCase):

    def setUp(self):
        self.table = StudentTable()
        self.table.create_record(1, "Иван", "Петров", 20, "М")
        self.table.create_record(2, "Мария", "Иванова", 22, "Ж")

    def test_select_by_id(self):
        result = self.table.select_record(student_id=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Иван")

    def test_select_by_first_name(self):
        result = self.table.select_record(first_name="мария")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 2)

    def test_select_by_second_name(self):
        result = self.table.select_record(second_name="петров")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)

    def test_select_by_age(self):
        result = self.table.select_record(age=20)
        self.assertEqual(len(result), 1)

    def test_select_by_sex(self):
        result = self.table.select_record(sex="ж")
        self.assertEqual(len(result), 1)

    def test_select_multiple_filters(self):
        result = self.table.select_record(age=20, sex="М")
        self.assertEqual(len(result), 1)

    def test_update_first_name(self):
        self.table.update_record(1, first_name="Иванн")
        result = self.table.select_record(student_id=1)
        self.assertEqual(result[0][1], "Иванн")

    def test_update_second_name(self):
        self.table.update_record(1, second_name="Сидоров")
        result = self.table.select_record(student_id=1)
        self.assertEqual(result[0][2], "Сидоров")

    def test_update_age(self):
        self.table.update_record(1, age=21)
        result = self.table.select_record(student_id=1)
        self.assertEqual(result[0][3], 21)

    def test_update_sex(self):
        self.table.update_record(2, sex="м")
        result = self.table.select_record(student_id=2)
        self.assertEqual(result[0][4], "М")

    def test_delete_one_record(self):
        self.table.delete_record(student_id=1)
        self.assertEqual(self.table.get_record_count(), 1)

    def test_delete_all_by_filter(self):
        self.table.delete_record(sex="М", delete_all=True)
        self.assertEqual(self.table.get_record_count(), 1)

    def test_validate_sex_upper(self):
        record = self.table.create_record(3, "Тест", "Тестов", 25, "M")
        self.assertEqual(record[4], "М")

    def test_validate_sex_lower(self):
        record = self.table.create_record(3, "Тест", "Тестов", 25, "м")
        self.assertEqual(record[4], "М")

    def test_invalid_age_negative(self):
        with self.assertRaises(InvalidAgeError):
            self.table.create_record(3, "Тест", "Тестов", -1, "М")

    def test_invalid_age_too_high(self):
        with self.assertRaises(InvalidAgeError):
            self.table.create_record(3, "Тест", "Тестов", 200, "М")

    def test_duplicate_id(self):
        with self.assertRaises(DuplicateIDError):
            self.table.create_record(1, "Тест", "Тестов", 25, "М")

    def test_empty_first_name(self):
        with self.assertRaises(InvalidNameError):
            self.table.create_record(3, "", "Тестов", 25, "М")

    def test_empty_second_name(self):
        with self.assertRaises(InvalidNameError):
            self.table.create_record(3, "Тест", "", 25, "М")

    def test_invalid_sex(self):
        with self.assertRaises(InvalidSexError):
            self.table.create_record(3, "Тест", "Тестов", 25, "X")

    def test_record_not_found_update(self):
        with self.assertRaises(RecordNotFoundError):
            self.table.update_record(999, first_name="Тест")

    def test_record_not_found_delete(self):
        result = self.table.delete_record(student_id=999)
        self.assertEqual(result, 0)

    def test_delete_no_filters(self):
        with self.assertRaises(ValueError):
            self.table.delete_record()

    def test_get_all_records(self):
        all_records = self.table.get_all_records()
        self.assertEqual(len(all_records), 2)

    def test_get_record_count(self):
        count = self.table.get_record_count()
        self.assertEqual(count, 2)


if __name__ == '__main__':
    unittest.main()