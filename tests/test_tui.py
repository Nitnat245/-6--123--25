import unittest
from unittest.mock import patch


class TestTUI(unittest.TestCase):

    def test_create_app(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            self.assertIsNotNone(app)

    def test_read_int_valid(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='42'):
            app = StudentTUI()
            result = app._read_int("test: ")
            self.assertEqual(result, 42)

    def test_read_int_invalid_then_valid(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', side_effect=['abc', '42']):
            app = StudentTUI()
            result = app._read_int("test: ")
            self.assertEqual(result, 42)

    def test_read_optional_int_valid(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='42'):
            app = StudentTUI()
            result = app._read_optional_int("test: ")
            self.assertEqual(result, 42)

    def test_read_optional_int_empty(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value=''):
            app = StudentTUI()
            result = app._read_optional_int("test: ")
            self.assertIsNone(result)

    def test_print_records_empty(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            with patch('builtins.print') as mock_print:
                app._print_records([])
                mock_print.assert_called_with("Записи не найдены.")

    def test_print_records_with_data(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            records = [(1, "Ivan", "Petrov", 20, "M")]
            with patch('builtins.print') as mock_print:
                app._print_records(records)
                self.assertTrue(mock_print.called)

    def test_print_menu(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            with patch('builtins.print') as mock_print:
                app._print_menu()
                self.assertTrue(mock_print.called)

    def test_add_student_requires_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._add_student()
                self.assertTrue(mock_print.called)

    def test_show_all_requires_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._show_all_students()
                self.assertTrue(mock_print.called)

    def test_find_students_requires_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._find_students()
                self.assertTrue(mock_print.called)

    def test_update_student_requires_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._update_student()
                self.assertTrue(mock_print.called)

    def test_delete_student_requires_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._delete_student()
                self.assertTrue(mock_print.called)


if __name__ == '__main__':
    unittest.main()

