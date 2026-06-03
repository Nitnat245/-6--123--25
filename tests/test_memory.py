import unittest
from src.db.backend.memory import MemoryDatabase


class TestMemory(unittest.TestCase):

    def setUp(self):
        self.db = MemoryDatabase()
        self.db.create_table("students", ("id", "first_name", "second_name", "age", "sex"))

    def test_create_record(self):
        self.db.insert_record("students",
                              {"id": 1, "first_name": "Ivan", "second_name": "Petrov", "age": 20, "sex": "M"})
        records = self.db.select_records("students")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 1)

    def test_select_all(self):
        self.db.insert_record("students",
                              {"id": 1, "first_name": "Ivan", "second_name": "Petrov", "age": 20, "sex": "M"})
        self.db.insert_record("students",
                              {"id": 2, "first_name": "Maria", "second_name": "Ivanova", "age": 22, "sex": "F"})
        records = self.db.select_records("students")
        self.assertEqual(len(records), 2)

