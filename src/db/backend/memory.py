"""
Модуль для работы с базой данных студентов в оперативной памяти.
Реализует CRUD операции (Create, Read, Update, Delete).
"""

# Определение типа для записи таблицы
type StudentRecord = tuple[int, str, str, int, str]

# Таблица Student представлена списком записей (кортежей)
Student: list[StudentRecord] = []


def create_record(
        student_id: int,
        first_name: str,
        second_name: str,
        age: int,
        sex: str,
) -> StudentRecord:
    """
    Создаёт новую запись и добавляет её в таблицу Student.
    """
    # Проверка корректности возраста
    if age < 0:
        raise ValueError("Поле age не может быть отрицательным.")

    # Проверка уникальности идентификатора
    if any(record[0] == student_id for record in Student):
        raise ValueError(f"Запись с id={student_id} уже существует.")

    # Проверка на пустые строки
    if not first_name.strip():
        raise ValueError("Имя не может быть пустым.")

    if not second_name.strip():
        raise ValueError("Фамилия не может быть пустой.")

    sex_upper = sex.strip().upper()

    if sex_upper in ['М', 'M', 'МУЖ', 'МУЖСКОЙ', 'MALE', 'MAN']:
        sex_normalized = 'М'
    elif sex_upper in ['Ж', 'F', 'ЖЕН', 'ЖЕНСКИЙ', 'FEMALE', 'WOMAN']:
        sex_normalized = 'Ж'
    else:
        raise ValueError("Пол должен быть указан как 'М' или 'Ж' (можно писать по-русски или по-английски).")


    new_record: StudentRecord = (
        student_id,
        first_name.strip().capitalize(),
        second_name.strip().capitalize(),
        age,
        sex.strip().upper(),
    )

    Student.append(new_record)
    return new_record


def select_record(
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
) -> list[StudentRecord]:
    """
    Выполняет выборку записей из таблицы Student по фильтрам.
    """
    # Если фильтры не заданы, возвращаем все записи
    if (
            student_id is None
            and first_name is None
            and second_name is None
            and age is None
            and sex is None
    ):
        return Student.copy()

    result: list[StudentRecord] = []

    for record in Student:
        # Проверка соответствия каждому фильтру
        if student_id is not None and record[0] != student_id:
            continue

        if first_name is not None and record[1].lower() != first_name.lower():
            continue

        if second_name is not None and record[2].lower() != second_name.lower():
            continue

        if age is not None and record[3] != age:
            continue

        if sex is not None and record[4].upper() != sex.upper():
            continue

        result.append(record)

    return result


def update_record(
        student_id: int,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
) -> StudentRecord:
    """
    Обновляет поля существующей записи по идентификатору.
    """
    # Поиск индекса записи
    record_index = None
    for i, record in enumerate(Student):
        if record[0] == student_id:
            record_index = i
            break

    if record_index is None:
        raise ValueError(f"Запись с id={student_id} не найдена.")

    current_record = Student[record_index]

    # Валидация новых значений
    if age is not None:
        if age < 0:
            raise ValueError("Поле age не может быть отрицательным.")

    if first_name is not None and not first_name.strip():
        raise ValueError("Имя не может быть пустым.")

    if second_name is not None and not second_name.strip():
        raise ValueError("Фамилия не может быть пустой.")

    if sex is not None and sex.strip().upper() not in ['М', 'Ж', 'M', 'F']:
        raise ValueError("Пол должен быть указан как 'М'/'M' или 'Ж'/'F'.")

    # Создаем обновленную запись
    updated_record: StudentRecord = (
        student_id,
        (first_name.strip().capitalize() if first_name is not None else current_record[1]),
        (second_name.strip().capitalize() if second_name is not None else current_record[2]),
        (age if age is not None else current_record[3]),
        (sex.strip().upper() if sex is not None else current_record[4]),
    )

    Student[record_index] = updated_record
    return updated_record


def delete_record(
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
        delete_all: bool = False,
) -> int:
    """
    Удаляет запись(и) из таблицы по заданным фильтрам.
    """
    # Проверка, что указан хотя бы один фильтр
    if (student_id is None and first_name is None and
            second_name is None and age is None and sex is None):
        raise ValueError("Необходимо указать хотя бы один фильтр для удаления.")

    # Находим записи для удаления
    records_to_delete = select_record(
        student_id=student_id,
        first_name=first_name,
        second_name=second_name,
        age=age,
        sex=sex
    )

    if not records_to_delete:
        return 0

    if delete_all:
        # Удаляем все найденные записи
        deleted_count = 0
        for record in records_to_delete:
            for i, r in enumerate(Student):
                if r == record:
                    Student.pop(i)
                    deleted_count += 1
                    break
        return deleted_count
    else:
        # Удаляем только первую найденную запись
        for i, record in enumerate(Student):
            if record == records_to_delete[0]:
                Student.pop(i)
                return 1

    return 0

