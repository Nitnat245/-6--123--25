from src.db.backend.memory import StudentTable
from src.db.backend.errors import (
    InvalidAgeError,
    DuplicateIDError,
    RecordNotFoundError,
    InvalidNameError,
    InvalidSexError
)

class StudentTUI:
    def __init__(self):
        self.table = StudentTable()
        self.running = True

    def _print_menu(self) -> None:
        print("\n" + "=" * 50)
        print("       БАЗА ДАННЫХ СТУДЕНТОВ")
        print("=" * 50)
        print("1. Добавить запись")
        print("2. Показать все записи")
        print("3. Найти записи по фильтру")
        print("4. Обновить запись")
        print("5. Удалить запись(и)")
        print("0. Выход")
        print("-" * 50)

    def _read_int(self, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_optional_int(self, prompt: str) -> int | None:
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число или оставьте поле пустым.")

    def _print_records(self, records: list) -> None:
        if not records:
            print("Записи не найдены.")
            return

        print(f"\nНайдено записей: {len(records)}")
        print("-" * 70)
        print(f"{'ID':<5} {'Имя':<15} {'Фамилия':<15} {'Возраст':<8} {'Пол':<5}")
        print("-" * 70)

        for record in records:
            print(f"{record[0]:<5} {record[1]:<15} {record[2]:<15} {record[3]:<8} {record[4]:<5}")

        print("-" * 70)

    def _add_student(self) -> None:
        print("\n" + "-" * 30)
        print("Добавление записи")
        print("-" * 30)

        try:
            student_id = self._read_int("ID студента: ")
            first_name = input("Имя: ").strip()
            second_name = input("Фамилия: ").strip()
            age = self._read_int("Возраст: ")
            sex = input("Пол (М/Ж): ").strip()

            record = self.table.create_record(student_id, first_name, second_name, age, sex)
            print(f"\n✓ Запись добавлена: {record}")

        except (InvalidAgeError, DuplicateIDError, InvalidNameError, InvalidSexError) as e:
            print(f"\n✗ Ошибка: {e}")

    def _show_all_students(self) -> None:
        print("\n" + "-" * 30)
        print("Все записи")
        print("-" * 30)
        self._print_records(self.table.get_all_records())

    def _find_students(self) -> None:
        print("\n" + "-" * 30)
        print("Поиск по фильтру")
        print("-" * 30)
        print("(Enter = пропустить поле)\n")

        student_id = self._read_optional_int("ID: ")
        first_name = input("Имя: ").strip() or None
        second_name = input("Фамилия: ").strip() or None
        age = self._read_optional_int("Возраст: ")
        sex = input("Пол (М/Ж): ").strip() or None

        records = self.table.select_record(
            student_id=student_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            sex=sex
        )

        self._print_records(records)

    def _update_student(self) -> None:
        print("\n" + "-" * 30)
        print("Обновление записи")
        print("-" * 30)

        student_id = self._read_int("ID студента для обновления: ")

        print("\nВведите новые значения (Enter = без изменений):")
        first_name = input("Новое имя: ").strip() or None
        second_name = input("Новая фамилия: ").strip() or None
        age = self._read_optional_int("Новый возраст: ")
        sex = input("Новый пол (М/Ж): ").strip() or None

        try:
            record = self.table.update_record(
                student_id=student_id,
                first_name=first_name,
                second_name=second_name,
                age=age,
                sex=sex
            )
            print(f"\n✓ Запись обновлена: {record}")

        except (RecordNotFoundError, InvalidAgeError, InvalidNameError, InvalidSexError) as e:
            print(f"\n✗ Ошибка: {e}")

    def _delete_student(self) -> None:
        print("\n" + "-" * 30)
        print("Удаление записей")
        print("-" * 30)
        print("Укажите критерии для удаления:")
        print("(Enter = пропустить поле)\n")

        student_id = self._read_optional_int("ID: ")
        first_name = input("Имя: ").strip() or None
        second_name = input("Фамилия: ").strip() or None
        age = self._read_optional_int("Возраст: ")
        sex = input("Пол (М/Ж): ").strip() or None

        if all(p is None for p in [student_id, first_name, second_name, age, sex]):
            print("\n✗ Ошибка: укажите хотя бы один критерий для удаления.")
            return

        records_to_delete = self.table.select_record(
            student_id=student_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            sex=sex
        )

        if not records_to_delete:
            print("\nЗаписи для удаления не найдены.")
            return

        print("\nБудут удалены:")
        self._print_records(records_to_delete)

        choice = input(f"\nУдалить {len(records_to_delete)} запись(ей)? (д/н): ").strip().lower()

        if choice not in ['д', 'да', 'y', 'yes']:
            print("Удаление отменено.")
            return

        if len(records_to_delete) > 1:
            delete_all_choice = input("Удалить ВСЕ найденные записи? (д/н): ").strip().lower()
            delete_all = delete_all_choice in ['д', 'да', 'y', 'yes']
        else:
            delete_all = True

        try:
            deleted_count = self.table.delete_record(
                student_id=student_id,
                first_name=first_name,
                second_name=second_name,
                age=age,
                sex=sex,
                delete_all=delete_all
            )
            print(f"\n✓ Удалено записей: {deleted_count}")
        except ValueError as e:
            print(f"\n✗ Ошибка: {e}")

    def run(self) -> None:
        print("\n" + "=" * 50)
        print("  УПРАВЛЕНИЕ БАЗОЙ ДАННЫХ СТУДЕНТОВ")
        print("=" * 50)

        while self.running:
            self._print_menu()
            action = input("Выберите действие (0-5): ").strip()

            if action == "1":
                self._add_student()
            elif action == "2":
                self._show_all_students()
            elif action == "3":
                self._find_students()
            elif action == "4":
                self._update_student()
            elif action == "5":
                self._delete_student()
            elif action == "0":
                print("\nДо свидания!")
                self.running = False
            else:
                print("\nНеизвестная команда. Выберите 0-5.")

            if self.running:
                input("\nНажмите Enter для продолжения...")