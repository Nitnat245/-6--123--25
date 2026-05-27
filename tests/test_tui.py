import unittest
from unittest.mock import patch, MagicMock


class TestTUI(unittest.TestCase):

    def test_import_and_create(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            self.assertIsNotNone(app)

    def test_select_memory_db(self):
        from src.db.tui import StudentTUI
        from src.db.backend.memory import MemoryDatabase
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            self.assertIsInstance(app.db, MemoryDatabase)

    def test_select_file_db(self):
        from src.db.tui import StudentTUI
        from src.db.backend.file import FileDatabase
        with patch('builtins.input', return_value='2'):
            app = StudentTUI()
            self.assertIsInstance(app.db, FileDatabase)

    def test_read_int_valid(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='123'):
            app = StudentTUI()
            result = app._read_int("test: ")
            self.assertEqual(result, 123)

    def test_read_int_invalid(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', side_effect=['abc', '456']):
            app = StudentTUI()
            result = app._read_int("test: ")
            self.assertEqual(result, 456)

    def test_read_optional_int_with_value(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='789'):
            app = StudentTUI()
            result = app._read_optional_int("test: ")
            self.assertEqual(result, 789)

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

    def test_add_student_no_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._add_student()
                mock_print.assert_called_with("Сначала создайте таблицу (пункт 1)")

    def test_show_all_no_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._show_all_students()
                mock_print.assert_called_with("Сначала создайте таблицу (пункт 1)")

    def test_find_students_no_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._find_students()
                mock_print.assert_called_with("Сначала создайте таблицу (пункт 1)")

    def test_update_student_no_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._update_student()
                mock_print.assert_called_with("Сначала создайте таблицу (пункт 1)")

    def test_delete_student_no_table(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            app.current_table = None
            with patch('builtins.print') as mock_print:
                app._delete_student()
                mock_print.assert_called_with("Сначала создайте таблицу (пункт 1)")

    def test_get_db_type_name(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', return_value='1'):
            app = StudentTUI()
            self.assertEqual(app.get_db_type_name(), 'MemoryDatabase')

    def test_run_exit(self):
        from src.db.tui import StudentTUI
        with patch('builtins.input', side_effect=['1', '0']):
            app = StudentTUI()
            app.run()


if __name__ == '__main__':
    unittest.main()