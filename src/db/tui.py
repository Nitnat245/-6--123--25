from .backend.memory import create_record, select_record, update_record,delete_record



def _print_menu() -> None:
    """Вывод текстового меню."""
    print("\n" + "=" * 40)
    print("       БАЗА ДАННЫХ СТУДЕНТОВ")
    print("=" * 40)
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("4. Обновить запись")
    print("5. Удалить запись(и)")
    print("0. Выход")
    print("-" * 40)


def _read_int(prompt: str) -> int:
    """Чтение целого числа из консоли."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")


def _print_records(records: list[tuple[int, str, str, int, str]]) -> None:
    """Вывод списка записей в отформатированном виде."""
    if not records:
        print("Записи не найдены.")
        return

    print(f"\nНайдено записей: {len(records)}")
    print("-" * 50)
    print(f"{'ID':<5} {'Имя':<15} {'Фамилия':<15} {'Возраст':<8} {'Пол':<5}")
    print("-" * 50)

    for record in records:
        print(f"{record[0]:<5} {record[1]:<15} {record[2]:<15} {record[3]:<8} {record[4]:<5}")

    print("-" * 50)


def _read_optional_int(prompt: str) -> int | None:
    """Чтение необязательного целого числа."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")


def _add_student() -> None:
    """Добавление нового студента."""
    print("\n" + "-" * 30)
    print("Добавление записи")
    print("-" * 30)

    student_id = _read_int("ID студента: ")
    first_name = input("Имя: ").strip()
    second_name = input("Фамилия: ").strip()
    age = _read_int("Возраст: ")
    sex = input("Пол (М/Ж): ").strip()

    try:
        record = create_record(student_id, first_name, second_name, age, sex)
        print(f"\n✓ Запись добавлена: {record}")
    except ValueError as exc:
        print(f"\n✗ Ошибка: {exc}")


def _show_all_students() -> None:
    """Показать всех студентов."""
    print("\n" + "-" * 30)
    print("Все записи")
    print("-" * 30)
    _print_records(select_record())


def _find_students_by_filter() -> None:
    """Поиск студентов по фильтру."""
    print("\n" + "-" * 30)
    print("Поиск по фильтру")
    print("-" * 30)
    print("(Enter = пропустить поле)\n")

    student_id = _read_optional_int("ID: ")
    first_name = input("Имя: ").strip() or None
    second_name = input("Фамилия: ").strip() or None
    age = _read_optional_int("Возраст: ")
    sex = input("Пол (М/Ж): ").strip() or None

    records = select_record(
        student_id=student_id,
        first_name=first_name,
        second_name=second_name,
        age=age,
        sex=sex,
    )

    _print_records(records)


def _update_student() -> None:
    """Обновление записи студента."""
    print("\n" + "-" * 30)
    print("Обновление записи")
    print("-" * 30)

    student_id = _read_int("ID студента для обновления: ")

    print("\nВведите новые значения (Enter = без изменений):")
    first_name = input("Новое имя: ").strip() or None
    second_name = input("Новая фамилия: ").strip() or None
    age = _read_optional_int("Новый возраст: ")
    sex = input("Новый пол (М/Ж): ").strip() or None

    try:
        record = update_record(
            student_id=student_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            sex=sex
        )
        print(f"\n✓ Запись обновлена: {record}")
    except ValueError as exc:
        print(f"\n✗ Ошибка: {exc}")


def _delete_student() -> None:
    """Удаление записи(ей) студента."""
    print("\n" + "-" * 30)
    print("Удаление записей")
    print("-" * 30)
    print("Укажите критерии для удаления:")
    print("(Enter = пропустить поле)\n")

    student_id = _read_optional_int("ID: ")
    first_name = input("Имя: ").strip() or None
    second_name = input("Фамилия: ").strip() or None
    age = _read_optional_int("Возраст: ")
    sex = input("Пол (М/Ж): ").strip() or None

    # Проверка, что указан хотя бы один критерий
    if (student_id is None and first_name is None and
            second_name is None and age is None and sex is None):
        print("\n✗ Ошибка: укажите хотя бы один критерий для удаления.")
        return

    # Показываем записи, которые будут удалены
    records_to_delete = select_record(
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
    _print_records(records_to_delete)

    # Подтверждение удаления
    choice = input(f"\nУдалить {len(records_to_delete)} запись(ей)? (д/н): ").strip().lower()

    if choice not in ['д', 'да', 'y', 'yes']:
        print("Удаление отменено.")
        return

    # Если записей больше одной, спрашиваем про удаление всех
    if len(records_to_delete) > 1:
        delete_all_choice = input("Удалить ВСЕ найденные записи? (д/н): ").strip().lower()
        delete_all = delete_all_choice in ['д', 'да', 'y', 'yes']
    else:
        delete_all = True

    try:
        deleted_count = delete_record(
            student_id=student_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            sex=sex,
            delete_all=delete_all
        )
        print(f"\n✓ Удалено записей: {deleted_count}")
    except ValueError as exc:
        print(f"\n✗ Ошибка: {exc}")


def run() -> None:
    """Запуск основного цикла программы."""
    print("\n" + "=" * 40)
    print("  УПРАВЛЕНИЕ БАЗОЙ ДАННЫХ СТУДЕНТОВ")
    print("=" * 40)

    while True:
        _print_menu()
        action = input("Выберите действие (0-5): ").strip()

        if action == "1":
            _add_student()
        elif action == "2":
            _show_all_students()
        elif action == "3":
            _find_students_by_filter()
        elif action == "4":
            _update_student()
        elif action == "5":
            _delete_student()
        elif action == "0":
            print("\nДо свидания!")
            break
        else:
            print("\nНеизвестная команда. Выберите 0-5.")

        input("\nНажмите Enter для продолжения...")