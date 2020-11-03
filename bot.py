from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3

from config import TOKEN
from db_operations import UsersData


if __name__ == "__main__":
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    DB_LOCATION = "database.db"


@dp.message_handler(commands=['start'])
async def process_start_command(message):
    await message.reply("Привет!\nНапиши мне свое имя, и я его запомню!")


@dp.message_handler(commands=['help'])
async def process_help_command(message):
    await message.reply("Я умею запоминать имена!")


@dp.message_handler()
async def message_to_person(message):
    with UsersData(DB_LOCATION) as db:
        name = db.get_username(message.from_user.id)
    if name:
        await bot.send_message(message.from_user.id,
            f"{name}, вы действительно считаете, что {message.text}?")
    else:
        with UsersData(DB_LOCATION) as db:
            db.set_username(message.from_user.id, message.text)
        await bot.send_message(
            message.from_user.id,
            f"Отлично, {message.text}, я запомнил твое имя."
        )


if __name__ == '__main__':
    executor.start_polling(dp)