from misc import dp, bot
from utils.db_operations import UsersData
from data.states import SET_EMAIL
from data.config import DB_LOCATION


@dp.message_handler(commands=['help'])
async def process_help_command(message):
    await message.reply("Для авторизации или изменения данных введите /start.")


@dp.message_handler(commands=['start'])
async def process_start_command(message):
    await bot.send_message(
        message.from_user.id,
        "Чтобы воспользоваться ботом пройдите авторизацию."
    )
    await bot.send_message(
        message.from_user.id,
        "Введите корпоративную почту."
    )
    
    with UsersData(DB_LOCATION) as db:
        db.set_state(message.from_user.id, SET_EMAIL)