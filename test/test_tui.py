import unittest
from unittest.mock import patch
from src.db.tui import StudentTUI


class TestTUI(unittest.TestCase):

    @patch('builtins.input', side_effect=['0'])
    def test_exit_program(self, mock_input):
        app = StudentTUI()
        app.run()

    @patch('builtins.input', side_effect=['1', 'students', '0'])
    def test_create_table(self, mock_input):
        app = StudentTUI()
        app.run()

    @patch('builtins.input', side_effect=['1', 'students', '2', '1', 'Иван', 'Петров', '20', 'М', '3', '0'])
    def test_add_and_show_records(self, mock_input):
        app = StudentTUI()
        app.run()


if __name__ == '__main__':
    unittest.main()