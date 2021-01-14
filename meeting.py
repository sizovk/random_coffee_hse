from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from data.states import *
from data.config import DB_LOCATION
from utils.db_operations import UsersData
from misc import dp, bot
from aiogram.utils import executor
from random import randint
from data.cities import cities


async def main():
    for city in cities:
        with UsersData(DB_LOCATION) as db:
            users = db.get_all_accept_meeting_from_city(city)
        pairs = pair_up(users)
        for pair in pairs:
            first_id = pair[0][0]
            first_social_network = pair[0][4]
            if len(pair) == 1:
                await bot.send_message(
                    first_id,
                    "К сожалению, мы не смогли подобрать вам пару на этой неделе.",
                )
                with UsersData(DB_LOCATION) as db:
                    db.set_state(first_id, AUTHORIZED)
                continue

            second_id = pair[1][0]
            second_social_network = pair[1][4]

            await bot.send_message(
                first_id,
                f"Мы подобрали вам пару, {second_social_network}",
            )
            with UsersData(DB_LOCATION) as db:
                db.set_state(first_id, AUTHORIZED)

            await bot.send_message(
                second_id,
                f"Мы подобрали вам пару, {first_social_network}",
            )
            with UsersData(DB_LOCATION) as db:
                db.set_state(second_id, AUTHORIZED)

            with UsersData(DB_LOCATION) as db:
                db.add_meeting(first_id, second_id)
        
        
def pair_up(users):
    pairs = list()
    for _ in range(len(users)):
        if len(users) == 0:
            break
        first = randint(0, len(users) - 1)
        second = randint(0, len(users) - 1)
        if first == second:
            continue
        if not met_before(users[first], users[second]):
            pairs.append([users[first], users[second]])
            users.pop(first)
            users.pop(second)
    for i in range(len(users)):
        pairs.append([users[i]])
    return pairs


def met_before(first_user, second_user):
    first_id = first_user[0]
    second_id = second_user[0]
    with UsersData(DB_LOCATION) as db:
        meeting = db.get_meeting(first_id, second_id)
        if len(meeting) == 0:
            return False
        return True


if __name__ == "__main__":
    executor.start(dp, main())