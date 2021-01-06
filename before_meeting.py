from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from data.states import *
from data.config import DB_LOCATION
from utils.db_operations import UsersData
from misc import dp, bot
from aiogram.utils import executor


async def main():
    with UsersData(DB_LOCATION) as db:
        users = db.get_all_authorized()
    
    keyboard = ReplyKeyboardMarkup()
    yes_button = KeyboardButton(text="Да")
    no_button = KeyboardButton(text="Нет")
    keyboard.add(yes_button)
    keyboard.add(no_button)
    for user in users:
        chat_id = user[0]
        await bot.send_message(
            chat_id,
            "Вы готовы к встрече на следующей неделе?\n",
            reply_markup=keyboard,
        )
        with UsersData(DB_LOCATION) as db:
            db.set_state(chat_id, BEFORE_MEETING)


if __name__ == "__main__":
    executor.start(dp, main())