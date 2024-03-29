import sqlite3
from data.states import AUTHORIZED, ACCEPT_MEETING


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
                state INTEGER,
                city TEXT,
                department TEXT,
                social_network TEXT,
                email TEXT,
                auth_code TEXT
        )""")
        self.__db_cursor.execute("""CREATE TABLE IF NOT EXISTS Meetings(
                first_id INTEGER,
                second_id INTEGER
        )""")
        self.__db_cursor.execute("""CREATE TABLE IF NOT EXISTS Future_meetings(
                first_id INTEGER,
                second_id INTEGER
        )""")
        self.commit()
    
    def __insert_user_if_not_in_db(self, chat_id):
        self.__db_cursor.execute(
            "INSERT OR IGNORE INTO Users(chat_id) VALUES(?)",
            (chat_id,)
        )

    def get_all_authorized(self):
        self.__db_cursor.execute(
            "SELECT * FROM Users WHERE state=?",
            (AUTHORIZED,)
        )
        items = self.__db_cursor.fetchall()
        return items

    def get_all_accept_meeting_from_city(self, city):
        self.__db_cursor.execute(
            "SELECT * FROM Users WHERE state=? AND city=?",
            (ACCEPT_MEETING, city,)
        )
        items = self.__db_cursor.fetchall()
        return items

    def set_city(self, chat_id, city):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "UPDATE Users SET city=? WHERE chat_id=?",
            (city, chat_id)
        )
        self.commit()

    def get_city(self, chat_id):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "SELECT city FROM Users WHERE chat_id=?",
            (chat_id,)
        )
        items = self.__db_cursor.fetchall()
        return items[0][0]

    def set_department(self, chat_id, department):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "UPDATE Users SET department=? WHERE chat_id=?",
            (department, chat_id)
        )
        self.commit()

    def get_department(self, chat_id):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "SELECT department FROM Users WHERE chat_id=?",
            (chat_id,)
        )
        items = self.__db_cursor.fetchall()
        return items[0][0]

    def set_social_network(self, chat_id, social_network):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "UPDATE Users SET social_network=? WHERE chat_id=?",
            (social_network, chat_id)
        )
        self.commit()

    def get_social_network(self, chat_id):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "SELECT social_network FROM Users WHERE chat_id=?",
            (chat_id,)
        )
        items = self.__db_cursor.fetchall()
        return items[0][0]

    def set_state(self, chat_id, state):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "UPDATE Users SET state=? WHERE chat_id=?",
            (state, chat_id)
        )
        self.commit()

    def get_state(self, chat_id):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "SELECT state FROM Users WHERE chat_id=?",
            (chat_id,)
        )
        items = self.__db_cursor.fetchall()
        return items[0][0]

    def set_email(self, chat_id, email):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "UPDATE Users SET email=? WHERE chat_id=?",
            (email, chat_id)
        )
        self.commit()

    def get_email(self, chat_id):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "SELECT email FROM Users WHERE chat_id=?",
            (chat_id,)
        )
        items = self.__db_cursor.fetchall()
        return items[0][0]

    def set_auth_code(self, chat_id, auth_code):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "UPDATE Users SET auth_code=? WHERE chat_id=?",
            (auth_code, chat_id)
        )
        self.commit()

    def get_auth_code(self, chat_id):
        self.__insert_user_if_not_in_db(chat_id)
        self.__db_cursor.execute(
            "SELECT auth_code FROM Users WHERE chat_id=?",
            (chat_id,)
        )
        items = self.__db_cursor.fetchall()
        return str(items[0][0])

    def add_meeting(self, first_id, second_id):
        if first_id > second_id:
            first_id, second_id = second_id, first_id
        self.__db_cursor.execute(
            "INSERT OR IGNORE INTO Meetings(first_id, second_id) VALUES(?, ?)",
            (first_id, second_id, )
        )
    
    def get_meeting(self, first_id, second_id):
        if first_id > second_id:
            first_id, second_id = second_id, first_id
        self.__db_cursor.execute(
            "SELECT * FROM Meetings WHERE first_id=? AND second_id=?",
            (first_id, second_id,)
        )
        items = self.__db_cursor.fetchall()
        return items

    def add_future_meeting(self, first_id, second_id):
        if first_id > second_id:
            first_id, second_id = second_id, first_id
        self.__db_cursor.execute(
            "INSERT OR IGNORE INTO Future_meetings(first_id, second_id) VALUES(?, ?)",
            (first_id, second_id,)
        )

    def get_future_meetings(self):
        self.__db_cursor.execute(
            "SELECT * FROM Future_meetings"
        )
        items = self.__db_cursor.fetchall()
        return items

    def clear_future_meetings(self):
        self.__db_cursor.execute(
            "DELETE FROM Future_meetings"
        )