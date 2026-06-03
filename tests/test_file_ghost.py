import unittest
import tempfile
from pathlib import Path
from src.db.backend.file import FileDatabase
from src.db.backend.database import Database
from src.db.backend.table import Table
from src.db.backend.errors import TableNotFoundError, TableAlreadyExistsError, InvalidStorageDataError, \
    MissingColumnError, UnknownColumnError


class TestFileDatabaseExtra(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = FileDatabase(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_multiple_tables(self):
        self.db.create_table("table1", ("id", "name"))
        self.db.create_table("table2", ("id", "age"))
        self.assertTrue(self.db._table_exists("table1"))
        self.assertTrue(self.db._table_exists("table2"))

    def test_insert_multiple_records(self):
        self.db.create_table("students", ("id", "name"))
        self.db.insert_record("students", {"id": 1, "name": "Ivan"})
        self.db.insert_record("students", {"id": 2, "name": "Maria"})
        self.db.insert_record("students", {"id": 3, "name": "Petr"})
        records = self.db.select_records("students")
        self.assertEqual(len(records), 3)

    def test_select_with_multiple_filters(self):
        self.db.create_table("students", ("id", "name", "age"))
        self.db.insert_record("students", {"id": 1, "name": "Ivan", "age": 20})
        self.db.insert_record("students", {"id": 2, "name": "Ivan", "age": 25})
        self.db.insert_record("students", {"id": 3, "name": "Maria", "age": 20})
        records = self.db.select_records("students", name="Ivan", age=20)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 1)

    def test_select_empty_result(self):
        self.db.create_table("students", ("id", "name"))
        records = self.db.select_records("students", name="Nonexistent")
        self.assertEqual(len(records), 0)

    def test_get_table_path_returns_path_object(self):
        path = self.db._get_table_path("test")
        self.assertIsInstance(path, Path)
        self.assertEqual(path.suffix, ".json")

    def test_serialize_table_with_empty_records(self):
        table = Table(("id", "name"))
        data = self.db._serialize_table(table)
        self.assertEqual(data["columns"], ["id", "name"])
        self.assertEqual(data["records"], [])

    def test_deserialize_table_with_empty_records(self):
        data = {"columns": ["id", "name"], "records": []}
        table = self.db._deserialize_table(data)
        self.assertEqual(len(table.records), 0)

    def test_deserialize_table_missing_columns_key(self):
        data = {"records": []}
        with self.assertRaises(InvalidStorageDataError):
            self.db._deserialize_table(data)

    def test_deserialize_table_missing_records_key(self):
        data = {"columns": ["id", "name"]}
        with self.assertRaises(InvalidStorageDataError):
            self.db._deserialize_table(data)

    def test_database_implements_abstract_methods(self):
        from src.db.backend.database import Database
        self.assertTrue(hasattr(FileDatabase, '_table_exists'))
        self.assertTrue(hasattr(FileDatabase, '_load_table'))
        self.assertTrue(hasattr(FileDatabase, '_save_table'))

    def test_file_extension_is_json(self):
        self.db.create_table("test", ("id",))
        path = self.db._get_table_path("test")
        self.assertEqual(path.suffix, ".json")

    def test_file_content_is_valid_json(self):
        import json
        self.db.create_table("test", ("id", "name"))
        self.db.insert_record("test", {"id": 1, "name": "Ivan"})

        path = self.db._get_table_path("test")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertIn("columns", data)
        self.assertIn("records", data)
        self.assertEqual(len(data["records"]), 1)


class TestTableExtra(unittest.TestCase):

    def test_table_columns_are_tuple(self):
        table = Table(("id", "name"))
        self.assertIsInstance(table.columns, tuple)

    def test_table_records_are_list(self):
        table = Table(("id", "name"))
        self.assertIsInstance(table.records, list)

    def test_insert_record_modifies_records(self):
        table = Table(("id", "name"))
        initial_count = len(table.records)
        table.insert_record({"id": 1, "name": "Ivan"})
        self.assertEqual(len(table.records), initial_count + 1)

    def test_insert_record_creates_copy(self):
        table = Table(("id", "name"))
        record = {"id": 1, "name": "Ivan"}
        table.insert_record(record)
        record["name"] = "Changed"
        self.assertEqual(table.records[0]["name"], "Ivan")

    def test_select_returns_copies(self):
        table = Table(("id", "name"))
        table.insert_record({"id": 1, "name": "Ivan"})
        records = table.select_records()
        records[0]["name"] = "Changed"
        self.assertEqual(table.records[0]["name"], "Ivan")

    def test_insert_multiple_records_different_columns(self):
        table = Table(("id", "name", "age"))
        table.insert_record({"id": 1, "name": "Ivan", "age": 20})
        table.insert_record({"id": 2, "name": "Maria", "age": 25})
        self.assertEqual(len(table.records), 2)

    def test_to_dict_returns_dict(self):
        table = Table(("id", "name"))
        data = table.to_dict()
        self.assertIsInstance(data, dict)

    def test_from_dict_returns_table(self):
        data = {"columns": ["id", "name"], "records": []}
        table = Table.from_dict(data)
        self.assertIsInstance(table, Table)


if __name__ == '__main__':
    unittest.main()

