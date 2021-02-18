from data.config import DB_LOCATION
from utils.db_operations import UsersData


if __name__ == "__main__":
    with open("users.txt", "w") as f:
        with UsersData(DB_LOCATION) as db:
            for user in db.get_all_accept_meeting_from_city("Москва"):
                f.write(str(user[0]) + " " + str(user[4]) + '\n')
