from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from misc import dp, bot
from utils.db_operations import UsersData
from data.states import *
from data.config import DB_LOCATION
import logic.meeting as meet
from utils.yaml_util import load_yml_file
from data.messages_base import messages_base


@dp.message_handler(lambda message: meet.is_before_meeting(message.from_user.id))
async def message_before_meeting(message):
    if message.text == 'Да':
        await bot.send_message(
            message.from_user.id,
            messages_base['accept_meeting'],
            reply_markup=ReplyKeyboardRemove(),
        )
        with UsersData(DB_LOCATION) as db:
            db.set_state(message.from_user.id, ACCEPT_MEETING)
    elif message.text == 'Нет':
        await bot.send_message(
            message.from_user.id,
            messages_base['not_accept_meeting'],
            reply_markup=ReplyKeyboardRemove(),
        )
        with UsersData(DB_LOCATION) as db:
            db.set_state(message.from_user.id, AUTHORIZED)
    else:
        await bot.send_message(
            message.from_user.id,
            messages_base['wrong_answer']
        )


@dp.message_handler(lambda message: meet.is_accept_meeting(message.from_user.id))
async def message_accept_meeting(message):
    await bot.send_message(
        message.from_user.id,
        messages_base['accept_meeting'],
    )