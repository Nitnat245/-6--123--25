import unittest
from src.db.backend.database import Database
from src.db.backend.memory import MemoryDatabase
from src.db.backend.file import FileDatabase
from src.db.backend.errors import TableNotFoundError, TableAlreadyExistsError


class TestDatabaseInterface(unittest.TestCase):

    def test_memory_implements_database(self):
        db = MemoryDatabase()
        self.assertIsInstance(db, Database)

    def test_file_implements_database(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            self.assertIsInstance(db, Database)

    def test_memory_create_table(self):
        db = MemoryDatabase()
        db.create_table("test", ("id", "name"))
        self.assertTrue(db._table_exists("test"))

    def test_memory_create_table_already_exists(self):
        db = MemoryDatabase()
        db.create_table("test", ("id", "name"))
        with self.assertRaises(TableAlreadyExistsError):
            db.create_table("test", ("id", "name"))

    def test_memory_insert_record(self):
        db = MemoryDatabase()
        db.create_table("test", ("id", "name"))
        db.insert_record("test", {"id": 1, "name": "Ivan"})
        records = db.select_records("test")
        self.assertEqual(len(records), 1)

    def test_memory_select_with_filter(self):
        db = MemoryDatabase()
        db.create_table("test", ("id", "name"))
        db.insert_record("test", {"id": 1, "name": "Ivan"})
        db.insert_record("test", {"id": 2, "name": "Maria"})
        records = db.select_records("test", name="Maria")
        self.assertEqual(len(records), 1)

    def test_memory_select_no_table(self):
        db = MemoryDatabase()
        with self.assertRaises(TableNotFoundError):
            db.select_records("nonexistent")

    def test_memory_insert_no_table(self):
        db = MemoryDatabase()
        with self.assertRaises(TableNotFoundError):
            db.insert_record("nonexistent", {"id": 1})


if __name__ == '__main__':
    unittest.main()

