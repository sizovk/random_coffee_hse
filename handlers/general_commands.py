from misc import dp, bot
from utils.db_operations import UsersData
from data.states import SET_EMAIL
from data.config import DB_LOCATION
from data.messages_base import messages_base


@dp.message_handler(commands=['help'])
async def process_help_command(message):
    await message.reply(messages_base['help_message'])


@dp.message_handler(commands=['start'])
async def process_start_command(message):
    await bot.send_message(
        message.from_user.id,
        messages_base['start_message']
    )
    await bot.send_message(
        message.from_user.id,
        messages_base['input_mail']
    )
    
    with UsersData(DB_LOCATION) as db:
        db.set_state(message.from_user.id, SET_EMAIL)