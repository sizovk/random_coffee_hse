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


def is_authorized(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == AUTHORIZED


def is_set_username_state(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == SET_USERNAME


def is_set_department_state(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == SET_DEPARTMENT


def is_not_authorized(chat_id):
    with UsersData(DB_LOCATION) as db:
        print(db.get_state(chat_id))
        return db.get_state(chat_id) == None


@dp.message_handler(commands=['start'])
async def process_start_command(message):
    await bot.send_message(
        message.from_user.id,
        "Чтобы воспользоваться ботом пройдите авторизацию."
    )
    await bot.send_message(
        message.from_user.id,
        "Введите свое имя."
    )
    with UsersData(DB_LOCATION) as db:
        db.set_state(message.from_user.id, SET_USERNAME)


@dp.message_handler(commands=['help'])
async def process_help_command(message):
    await message.reply("Для авторизации или изменения данных введите /start.")


@dp.message_handler(lambda message: is_authorized(message.from_user.id))
async def message_to_authorized_person(message):
    with UsersData(DB_LOCATION) as db:
        name = db.get_username(message.from_user.id)
        department = db.get_department(message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        f"Вы прошли авторизацию.\n\
        Ваше имя - {name}\n\
        Ваш факультет - {department}."
    )


@dp.message_handler(lambda message: is_set_username_state(message.from_user.id))
async def set_username_message(message):
    with UsersData(DB_LOCATION) as db:
        db.set_username(message.from_user.id, message.text)
    await bot.send_message(
        message.from_user.id,
        f"Введите название Вашего факультета."
    )
    with UsersData(DB_LOCATION) as db:
        db.set_state(message.from_user.id, SET_DEPARTMENT)


@dp.message_handler(lambda message: is_set_department_state(message.from_user.id))
async def set_department_message(message):
    with UsersData(DB_LOCATION) as db:
        db.set_department(message.from_user.id, message.text)
    with UsersData(DB_LOCATION) as db:
        db.set_state(message.from_user.id, AUTHORIZED)
        await bot.send_message(
        message.from_user.id,
        "Авторизация завершена."
    )


@dp.message_handler(lambda message: is_not_authorized(message.from_user.id))
async def message_to_not_authorized_person(message):
    await bot.send_message(
        message.from_user.id,
        "Вам необходимо пройти авторизацию.\n\
        Для уточнения подробностей введите /start."
    )


if __name__ == '__main__':
    executor.start_polling(dp)