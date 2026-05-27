import unittest


class TestSimple(unittest.TestCase):

    def test_import_memory(self):
        from src.db.backend.memory import StudentTable
        self.assertIsNotNone(StudentTable)

    def test_import_errors(self):
        from src.db.backend.errors import InvalidAgeError
        self.assertIsNotNone(InvalidAgeError)


    def test_import_tui(self):
        from src.db.tui import StudentTUI
        self.assertIsNotNone(StudentTUI)



if __name__ == '__main__':
    unittest.main()
