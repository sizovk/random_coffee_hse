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
    while len(users) >= 2:
        pair = []
        first = randint(0, len(users) - 1)
        pair.append(users[first])
        users.pop(first)
        second = randint(0, len(users) - 1)
        pair.append(users[second])
        users.pop(second)
        pairs.append(pair)
    if len(users) == 1:
        pairs.append([users[0]])
    return pairs


if __name__ == "__main__":
    executor.start(dp, main())