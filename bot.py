from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3

from config import TOKEN


def create_table(connection):
    cursorObj = connection.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, name text)")
    connection.commit()


def get_name_by_user_id(user_id, connection):
    cursorObj = connection.cursor()
    cursorObj.execute(f'SELECT name FROM users WHERE id == {user_id}')
    response = cursorObj.fetchall()
    if response:
        return response[0][0]
    else:
        return ""


def set_name_into_table(user_id, name, connection):
    cursorObj = connection.cursor()
    cursorObj.execute(
            "INSERT INTO users VALUES(?, ?)",
            (user_id, name)
        )
    connection.commit()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
connection = sqlite3.connect("database.db")
create_table(connection)


@dp.message_handler(commands=['start'])
async def process_start_command(message):
    await message.reply("Привет!\nНапиши мне свое имя, и я его запомню!")


@dp.message_handler(commands=['help'])
async def process_help_command(message):
    await message.reply("Я умею запоминать имена!")


@dp.message_handler()
async def message_to_person(message):
    name = get_name_by_user_id(message.from_user.id, connection)
    if name:
        await bot.send_message(message.from_user.id,
            f"{name}, вы действительно считаете, что {message.text}?")
    else:
        set_name_into_table(message.from_user.id, message.text, connection)
        await bot.send_message(
            message.from_user.id,
            f"Отлично, {message.text}, я запомнил твое имя."
        )


if __name__ == '__main__':
    executor.start_polling(dp)