class DatabaseError(Exception):
    """Класс для ошибок базы данных."""
    pass

class TableAlreadyExistsError(DatabaseError):
    """Ошибка при создании уже существующей таблицы."""
    pass

class TableNotFoundError(DatabaseError):
    """Ошибка при обращении к несуществующей таблицееее 0.0"""
    pass

class MissingColumnError(DatabaseError):
    """Ошибка при отсутствии обязательного поля."""
    pass

class UnknownColumnError(DatabaseError):
    """Ошибка при использовании поля, которого нет в схеме."""
    pass

class InvalidStorageDataError(DatabaseError):
    """Ошибка при чтении повреждённых данных из файла."""
    pass



class InvalidAgeError(DatabaseError):
    pass

class DuplicateIDError(DatabaseError):
    pass

class RecordNotFoundError(DatabaseError):
    pass

class InvalidNameError(DatabaseError):
    pass

class InvalidSexError(DatabaseError):
    pass