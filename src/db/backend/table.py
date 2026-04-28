from typing import Any
from .errors import MissingColumnError, UnknownColumnError

class Table:
    def __init__(self, columns: tuple[str, ...]) -> None:
        self.columns = columns
        self.records: list[dict[str, Any]] = []

    def insert_record(self, record: dict[str, Any]) -> None:
        # Проверяем, что есть все поля
        for col in self.columns:
            if col not in record:
                raise MissingColumnError(f"Отсутствует поле '{col}'")
        # Проверяем, что нет лишних полей
        for key in record:
            if key not in self.columns:
                raise UnknownColumnError(f"Поле '{key}' не определено")
        self.records.append(record.copy())
        print(f"Запись добавлена. Всего записей: {len(self.records)}")

    def select_records(self, **filters: Any) -> list[dict[str, Any]]:
        for key in filters:
            if key not in self.columns:
                raise UnknownColumnError(f"Поле '{key}' не определено")
        if not filters:
            return [r.copy() for r in self.records]
        result = []
        for record in self.records:
            if all(record.get(k) == v for k, v in filters.items()):
                result.append(record.copy())
        return result

    def get_all_records(self) -> list[dict[str, Any]]:
        return [r.copy() for r in self.records]

    def to_dict(self) -> dict:
        return {
            "columns": list(self.columns),
            "records": self.records.copy()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Table':
        table = cls(tuple(data["columns"]))
        table.records = data["records"].copy()
        return table