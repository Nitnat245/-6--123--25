import tempfile
import unittest
from src.db.backend.file import FileDatabase
from src.db.backend.errors import TableNotFoundError, TableAlreadyExistsError


class TestFileDatabase(unittest.TestCase):
    def test_data_saved_between_instances(self):
        with tempfile.TemporaryDirectory() as d:
            db1 = FileDatabase(d)
            db1.create_table("students", ("id", "name"))
            db1.insert_record("students", {"id": 1, "name": "Ivan"})

            db2 = FileDatabase(d)
            records = db2.select_records("students")
            self.assertEqual(records, [{"id": 1, "name": "Ivan"}])

    def test_select_with_filter(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            db.create_table("students", ("id", "name"))
            db.insert_record("students", {"id": 1, "name": "Ivan"})
            db.insert_record("students", {"id": 2, "name": "Maria"})
            records = db.select_records("students", name="Maria")
            self.assertEqual(records, [{"id": 2, "name": "Maria"}])

    def test_missing_table_error(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            with self.assertRaises(TableNotFoundError):
                db.select_records("students")

    def test_create_existing_table_error(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            db.create_table("students", ("id", "name"))
            with self.assertRaises(TableAlreadyExistsError):
                db.create_table("students", ("id", "name"))


if __name__ == "__main__":
    unittest.main()