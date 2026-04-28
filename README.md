

Добромыслова Василиса  
М6О-123БВ-25


## memory.py

`MemoryDatabase` — класс для хранения данных в оперативной памяти.

- `create_table()` — создаёт таблицу
- `insert_record()` — добавляет запись
- `select_records()` — выполняет поиск записей



## file.py

`FileDatabase` — класс для хранения данных в JSON-файлах.

- `create_table()` — создаёт таблицу и сохраняет в файл
- `insert_record()` — добавляет запись и сохраняет в файл
- `select_records()` — выполняет поиск записей


## table.py

`Table` — класс для работы со структурой таблицы.

- `insert_record()` — добавляет запись с проверкой полей
- `select_records()` — возвращает записи по фильтрам
- `to_dict()` — преобразует таблицу в словарь
- `from_dict()` — создаёт таблицу из словаря

## errors.py

Пользовательские исключения:

- `TableAlreadyExistsError` — таблица уже существует
- `TableNotFoundError` — таблица не найдена
- `MissingColumnError` — отсутствует обязательное поле
- `UnknownColumnError` — присутствует неизвестное поле
- `InvalidStorageDataError` — файл повреждён

## tui.py

`StudentTUI` — класс текстового интерфейса.

- `_select_database()` — выбор типа базы данных
- `_create_table()` — создание таблицы
- `_add_record()` — добавление записи
- `_show_all()` — отображение всех записей





