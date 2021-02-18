from data.config import DB_LOCATION
from data.states import AUTHORIZED
from utils.db_operations import UsersData
from misc import dp, bot
from aiogram.utils import executor


async def main():
    first_id = 326131979
    second_id = 737441938
    with UsersData(DB_LOCATION) as db:
        first_social_network = db.get_social_network(first_id)
        second_social_network = db.get_social_network(second_id)
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


if __name__ == "__main__":
    executor.start(dp, main())