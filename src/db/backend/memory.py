from .errors import DuplicateIDError, InvalidAgeError, RecordNotFoundError, InvalidNameError, InvalidSexError

type StudentRecord = tuple[int, str, str, int, str]

class StudentTable:
    def __init__(self) -> None:
        self._students: list[StudentRecord] = []

    def _validate_name(self, name: str, field_name: str = "Имя") -> str:
        cleaned = name.strip()
        if not cleaned:
            raise InvalidNameError(f"{field_name} не может быть пустым.")
        return cleaned.capitalize()

    def _validate_age(self, age: int) -> int:
        if age < 0:
            raise InvalidAgeError("Возраст не может быть отрицательным.")
        if age > 150:
            raise InvalidAgeError("Возраст не может быть больше 150.")
        return age

    def _validate_sex(self, sex: str) -> str:
        sex_upper = sex.strip().upper()
        if sex_upper in ['М', 'M', 'МУЖ', 'MALE', 'MAN']:
            return 'М'
        elif sex_upper in ['Ж', 'F', 'FEMALE', 'WOMAN']:
            return 'Ж'
        else:
            raise InvalidSexError("Пол должен быть указан как 'М' или 'Ж'.")

    def _check_unique_id(self, student_id: int) -> None:
        if any(record[0] == student_id for record in self._students):
            raise DuplicateIDError(f"Запись с id={student_id} уже существует.")

    def _find_record_index(self, student_id: int) -> int:
        for i, record in enumerate(self._students):
            if record[0] == student_id:
                return i
        raise RecordNotFoundError(f"Запись с id={student_id} не найдена.")

    def create_record(self, student_id: int, first_name: str, second_name: str, age: int, sex: str) -> StudentRecord:
        self._check_unique_id(student_id)
        validated_age = self._validate_age(age)
        validated_first_name = self._validate_name(first_name, "Имя")
        validated_second_name = self._validate_name(second_name, "Фамилия")
        validated_sex = self._validate_sex(sex)

        new_record: StudentRecord = (student_id, validated_first_name, validated_second_name, validated_age, validated_sex)
        self._students.append(new_record)
        return new_record

    def select_record(self, student_id: int | None = None, first_name: str | None = None,
                      second_name: str | None = None, age: int | None = None, sex: str | None = None) -> list[StudentRecord]:
        if all(param is None for param in [student_id, first_name, second_name, age, sex]):
            return self._students.copy()

        result: list[StudentRecord] = []
        for record in self._students:
            if student_id is not None and record[0] != student_id:
                continue
            if first_name is not None and record[1].lower() != first_name.lower():
                continue
            if second_name is not None and record[2].lower() != second_name.lower():
                continue
            if age is not None and record[3] != age:
                continue
            if sex is not None:
                normalized_sex = self._validate_sex(sex)
                if record[4] != normalized_sex:
                    continue
            result.append(record)
        return result

    def update_record(self, student_id: int, first_name: str | None = None,
                      second_name: str | None = None, age: int | None = None, sex: str | None = None) -> StudentRecord:
        index = self._find_record_index(student_id)
        current = self._students[index]

        new_first = self._validate_name(first_name, "Имя") if first_name is not None else current[1]
        new_second = self._validate_name(second_name, "Фамилия") if second_name is not None else current[2]
        new_age = self._validate_age(age) if age is not None else current[3]
        new_sex = self._validate_sex(sex) if sex is not None else current[4]

        updated: StudentRecord = (student_id, new_first, new_second, new_age, new_sex)
        self._students[index] = updated
        return updated

    def delete_record(self, student_id: int | None = None, first_name: str | None = None,
                      second_name: str | None = None, age: int | None = None, sex: str | None = None,
                      delete_all: bool = False) -> int:
        if all(p is None for p in [student_id, first_name, second_name, age, sex]):
            raise ValueError("Нужно указать хотя бы один фильтр")

        to_delete = self.select_record(student_id, first_name, second_name, age, sex)
        if not to_delete:
            return 0

        if not delete_all:
            to_delete = [to_delete[0]]

        deleted = 0
        for record in to_delete:
            for i, r in enumerate(self._students):
                if r == record:
                    self._students.pop(i)
                    deleted += 1
                    break
        return deleted

    def get_all_records(self) -> list[StudentRecord]:
        return self._students.copy()

    def get_record_count(self) -> int:
        return len(self._students)