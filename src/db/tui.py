from src.db.backend.memory import MemoryDatabase
from src.db.backend.file import FileDatabase
from src.db.backend.errors import (
    TableNotFoundError, TableAlreadyExistsError,
    MissingColumnError, UnknownColumnError
)

class StudentTUI:
    def __init__(self):
        self.database = self._select_database()
        self.current_table = None
        self.running = True

    def _select_database(self):
        print("\n" + "=" * 50)
        print("     ВЫБОР ТИПА БАЗЫ ДАННЫХ")
        print("=" * 50)
        print("1. In-memory (данные не сохраняются)")
        print("2. File (данные сохраняются в JSON файлы)")
        print("-" * 50)
        choice = input("Выберите тип (1 или 2): ").strip()
        if choice == "2":
            print("\n✓ Выбрана файловая база данных. Данные будут сохранены в папке 'data/'")
            return FileDatabase()
        else:
            print("\n✓ Выбрана in-memory база данных. Данные будут потеряны после выхода")
            return MemoryDatabase()

    def _print_menu(self):
        print("\n" + "=" * 50)
        print("       БАЗА ДАННЫХ СТУДЕНТОВ")
        print("=" * 50)
        if self.current_table:
            print(f"Текущая таблица: {self.current_table}")
        else:
            print("Таблица не создана")
        print("-" * 50)
        print("1. Создать таблицу")
        print("2. Добавить запись")
        print("3. Показать все записи")
        print("4. Найти записи по фильтру")
        print("0. Выход")
        print("-" * 50)

    def _read_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Ошибка: введите число")

    def _create_table(self):
        name = input("Имя таблицы: ").strip()
        if not name:
            print("Ошибка: имя не может быть пустым")
            return
        columns = ("id", "first_name", "second_name", "age", "sex")
        try:
            self.database.create_table(name, columns)
            self.current_table = name
            print(f"✓ Таблица '{name}' создана")
        except TableAlreadyExistsError as e:
            print(f"Ошибка: {e}")

    def _add_record(self):
        if not self.current_table:
            print("Сначала создайте таблицу (пункт 1)")
            return
        try:
            record = {
                "id": self._read_int("ID: "),
                "first_name": input("Имя: ").strip(),
                "second_name": input("Фамилия: ").strip(),
                "age": self._read_int("Возраст: "),
                "sex": input("Пол (М/Ж): ").strip()
            }
            self.database.insert_record(self.current_table, record)
            print("Запись добавлена")
        except (MissingColumnError, UnknownColumnError) as e:
            print(f"Ошибка: {e}")

    def _show_all(self):
        if not self.current_table:
            print("Сначала создайте таблицу (пункт 1)")
            return
        records = self.database.select_records(self.current_table)
        if not records:
            print("Записей нет")
            return
        print(f"\nВсего записей: {len(records)}")
        print("-" * 70)
        print(f"{'ID':<5} {'Имя':<15} {'Фамилия':<15} {'Возраст':<8} {'Пол':<5}")
        print("-" * 70)
        for r in records:
            print(f"{r['id']:<5} {r['first_name']:<15} {r['second_name']:<15} {r['age']:<8} {r['sex']:<5}")
        print("-" * 70)

    def _find_records(self):
        if not self.current_table:
            print("Сначала создайте таблицу (пункт 1)")
            return
        print("\n(Enter = пропустить поле)")
        filters = {}
        id_val = input("ID: ").strip()
        if id_val:
            filters["id"] = int(id_val)
        name = input("Имя: ").strip()
        if name:
            filters["first_name"] = name
        sname = input("Фамилия: ").strip()
        if sname:
            filters["second_name"] = sname
        age = input("Возраст: ").strip()
        if age:
            filters["age"] = int(age)
        sex = input("Пол: ").strip()
        if sex:
            filters["sex"] = sex
        records = self.database.select_records(self.current_table, **filters)
        if not records:
            print("Записи не найдены")
            return
        print(f"\nНайдено: {len(records)}")
        for r in records:
            print(r)

    def run(self):
        while self.running:
            self._print_menu()
            choice = input("Выберите действие (0-4): ").strip()
            if choice == "1":
                self._create_table()
            elif choice == "2":
                self._add_record()
            elif choice == "3":
                self._show_all()
            elif choice == "4":
                self._find_records()
            elif choice == "0":
                print("До свидания!")
                self.running = False
            else:
                print("Неизвестная команда")
            if self.running:
                input("\nНажмите Enter...")