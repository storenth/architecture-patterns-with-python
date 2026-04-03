from abc import ABC, abstractmethod

class DBConnectionInterface(ABC):
    """Интерфейс для подключения к базе данных"""
    @abstractmethod
    def connect(self) -> str:
        """Устанавливает соединение с БД"""
        pass

class MySQLConnection(DBConnectionInterface):
    def connect(self) -> str:
        """Handle the database connection"""
        return 'Database connection established'

class PasswordReminder:
    def __init__(self, db_connection: DBConnectionInterface):
        self.db_connection = db_connection
