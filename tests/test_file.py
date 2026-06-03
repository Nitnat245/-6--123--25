import unittest
import tempfile
from src.db.backend.file import FileDatabase


class TestFile(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = FileDatabase(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_table(self):
        self.db.create_table("students", ("id", "name"))
        self.assertTrue(self.db._table_exists("students"))


if __name__ == '__main__':
    unittest.main()

