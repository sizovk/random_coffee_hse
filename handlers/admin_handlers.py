from misc import dp, bot
from utils.db_operations import UsersData
from data.states import ADMIN_MEET, AUTHORIZED
from data.config import DB_LOCATION, ADMINS
from data.yml_config import messages_base


@dp.message_handler(commands=['list'])
async def process_list_command(message):
    if message.from_user.id not in ADMINS:
        await bot.send_message(
            message.from_user.id,
            messages_base['not_admin']
        )
    else:
        list = "List:\n"
        with UsersData(DB_LOCATION) as db:
            for user in db.get_all_accept_meeting_from_city("Москва"):
                list += str(user[0]) + " " + str(user[4]) + '\n'
        await bot.send_message(
            message.from_user.id,
            list
        )


@dp.message_handler(commands=['meet'])
async def process_list_command(message):
    if message.from_user.id not in ADMINS:
        await bot.send_message(
            message.from_user.id,
            messages_base['not_admin']
        )
    else:
        with UsersData(DB_LOCATION) as db:
            db.set_state(message.from_user.id, ADMIN_MEET)
        await bot.send_message(
            message.from_user.id,
            "Введите id."
        )


@dp.message_handler(lambda message: is_admin_meet(message.from_user.id))
async def process_list_command(message):
    first_id = message.from_user.id
    second_id = int(message.text)
    with UsersData(DB_LOCATION) as db:
        db.add_future_meeting(first_id, second_id)
    await bot.send_message(
        message.from_user.id,
        "Успешно."
    )
    with UsersData(DB_LOCATION) as db:
        db.set_state(first_id, AUTHORIZED)
        db.set_state(second_id, AUTHORIZED)


def is_admin_meet(chat_id):
    with UsersData(DB_LOCATION) as db:
        if db.get_state(chat_id) == ADMIN_MEET:
            return True
        else:
            return False