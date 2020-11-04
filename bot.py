from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3

from config import TOKEN
from db_operations import UsersData
from states import *


if __name__ == "__main__":
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    DB_LOCATION = "database.db"


@dp.message_handler(commands=['start'])
async def process_start_command(message):
    await message.reply("Привет!\nНапиши /help, чтобы узнать о боте больше!")


@dp.message_handler(commands=['help'])
async def process_help_command(message):
    await message.reply("Для авторизации или изменения данных есть следующие команды:\n\
    /name - изменить имя\n\
    /department - изменить факультет")

@dp.message_handler(commands=['name'])
async def process_name_command(message):
    await message.reply("Введите свое имя.")
    with UsersData(DB_LOCATION) as db:
        db.set_state(message.from_user.id, SET_USERNAME)


@dp.message_handler(commands=['department'])
async def process_department_command(message):
    await message.reply("Введите название своего факультета.")
    with UsersData(DB_LOCATION) as db:
        db.set_state(message.from_user.id, SET_DEPARTMENT)

@dp.message_handler()
async def message_to_person(message):
    with UsersData(DB_LOCATION) as db:
        state = db.get_state(message.from_user.id)
        db.set_state(message.from_user.id, NON_AUTHORIZED)
        if state == AUTHORIZED:
            name = db.get_username(message.from_user.id)
            department = db.get_department(message.from_user.id)
            await bot.send_message(
                message.from_user.id,
                f"Вы прошли авторизацию.\n\
                Ваше имя - {name}\n\
                Ваш факультет - {department}."
            )
        elif state == NON_AUTHORIZED:
            await bot.send_message(
                message.from_user.id,
                "Вам необходимо пройти авторизацию.\n\
                Для уточнения подробностей введите /help."
            )
        elif state == SET_USERNAME:
            db.set_username(message.from_user.id, message.text)
            await bot.send_message(
                message.from_user.id,
                f"Ваше имя - {message.text}"
            )
        elif state == SET_DEPARTMENT:
            db.set_department(message.from_user.id, message.text)
            await bot.send_message(
                message.from_user.id,
                f"Ваше факультет - {message.text}"
            )
        db.authorize(message.from_user.id)


if __name__ == '__main__':
    executor.start_polling(dp)