class StudentTableError(Exception):
    pass

class InvalidAgeError(StudentTableError):
    pass

class DuplicateIDError(StudentTableError):
    pass

class RecordNotFoundError(StudentTableError):
    pass

class InvalidNameError(StudentTableError):
    pass

class InvalidSexError(StudentTableError):
    pass


