from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from data.states import *
from data.config import DB_LOCATION, MAX_FAILURES
from utils.db_operations import UsersData
from misc import dp, bot
from aiogram.utils import executor
from random import randint, choice
from data.cities import cities
from data.messages_base import messages_base


async def main():
    for city in cities:
        with UsersData(DB_LOCATION) as db:
            users = db.get_all_accept_meeting_from_city(city)
        pairs = pair_up(set(users))
        for pair in pairs:
            first_id = pair[0][0]
            first_social_network = pair[0][4]
            if len(pair) == 1:
                await bot.send_message(
                    first_id,
                    messages_base['unsuccessful_matching'],
                )
                with UsersData(DB_LOCATION) as db:
                    db.set_state(first_id, AUTHORIZED)
                continue

            second_id = pair[1][0]
            second_social_network = pair[1][4]

            await bot.send_message(
                first_id,
                messages_base['successful_matching'].format(social_network=second_social_network),
            )
            with UsersData(DB_LOCATION) as db:
                db.set_state(first_id, AUTHORIZED)

            await bot.send_message(
                second_id,
                messages_base['successful_matching'].format(social_network=first_social_network),
            )
            with UsersData(DB_LOCATION) as db:
                db.set_state(second_id, AUTHORIZED)

            with UsersData(DB_LOCATION) as db:
                db.add_meeting(first_id, second_id)
        
        
def pair_up(users):
    pairs = list()
    failures = 0
    while failures < MAX_FAILURES:
        if len(users) < 2:
            break
        first_user = choice(tuple(users))
        users.remove(first_user)
        second_user = choice(tuple(users))
        users.remove(second_user)
        if not met_before(first_user, second_user):
            pairs.append([first_user, second_user])
            failures = 0
        else:
            failures += 1
            users.add(first_user)
            users.add(second_user)
    for user in users:
        pairs.append([user, ])
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