import json
from pathlib import Path
from .database import Database
from .errors import TableNotFoundError, InvalidStorageDataError
from .table import Table

class FileDatabase(Database):
    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        print(f"Папка для данных: {self.directory.absolute()}")

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        path = self._get_table_path(table_name)
        print(f"Загрузка таблицы из: {path}")
        if not path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"Загружено {len(data.get('records', []))} записей")
            return Table.from_dict(data)
        except json.JSONDecodeError as e:
            raise InvalidStorageDataError(f"Ошибка чтения JSON: {e}")

    def _save_table(self, table_name: str, table: Table) -> None:
        path = self._get_table_path(table_name)
        print(f"Сохранение таблицы в: {path}")
        print(f"Сохраняется {len(table.records)} записей")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(table.to_dict(), f, ensure_ascii=False, indent=2)
        print("Сохранение завершено")