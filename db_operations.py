import sqlite3


class UsersData:

    def __init__(self, db_location):
        self.__DB_LOCATION = db_location
        self.__db_connection = sqlite3.connect(db_location)
        self.__db_cursor = self.__db_connection.cursor()
        self.__create_table_if_not_exists()

    def __del__(self):
        self.__db_connection.close()

    def __enter__(self):
        return self
    
    def __exit__(self, ext_type, exc_value, traceback):
        self.__db_cursor.close()
        if isinstance(exc_value, Exception):
            self.__db_connection.rollback()
        else:
            self.__db_connection.commit()
        self.__db_connection.close()

    def commit(self):
        self.__db_connection.commit()

    def close(self):
        self.__db_connection.close()

    def __create_table_if_not_exists(self):
        self.__db_cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                chat_id INTEGER NOT NULL UNIQUE,
                name TEXT
        )""")
        self.commit()
    
    def __insert_user_if_not_in_db(self, chat_id):
        self.__db_cursor.execute(
            "INSERT OR IGNORE INTO Users(chat_id) VALUES(?)",
            (chat_id,)
        )

    def set_username(self, chat_id, name):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "UPDATE Users SET name=? WHERE chat_id=?",
            (name, chat_id)
        )
        self.commit()

    def get_username(self, chat_id):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "SELECT name FROM Users WHERE chat_id=?",
            (chat_id,)
        )
        items = self.__db_cursor.fetchall()
        return items[0][0]