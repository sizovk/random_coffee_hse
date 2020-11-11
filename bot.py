from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from random import randint
import smtplib

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

def is_set_email_state(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == SET_EMAIL

def is_set_code_authorization_state(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == SET_CODE_AUTHORIZATION

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


def is_correct_email(email):
    correct_suffixes = ["@hse.ru", "@edu.hse.ru"]
    for suffix in correct_suffixes:
        if len(email) > len(suffix):
            if email[-len(suffix):] == suffix:
                return True
    return False


def is_correct_auth_code(auth_code, chat_id):
    with UsersData(DB_LOCATION) as db:
        correct_auth_code = db.get_auth_code(chat_id)
    return (auth_code == correct_auth_code)


def send_auth_code(chat_id):
    auth_code = randint(1000, 9999)
    with UsersData(DB_LOCATION) as db:
        db.set_auth_code(chat_id, auth_code)
    with UsersData(DB_LOCATION) as db:
        email = db.get_email(chat_id)

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login("randomcoffeehse@gmail.com", "qwerty!23")
    subject = "Authorization code"
    to_email = email
    from_email = "randomcoffeehse@gmail.com"
    text = str(auth_code)
    body = "\r\n".join((
    f"From: {from_email}",
    f"To: {to_email}",
    f"Subject: {subject}",
    "",
    text
    ))
    smtpObj.sendmail(from_email, [to_email], body)
    smtpObj.quit()


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


@dp.message_handler(lambda message: is_authorized(message.from_user.id))
async def message_to_authorized_person(message):
    with UsersData(DB_LOCATION) as db:
        name = db.get_username(message.from_user.id)
        department = db.get_department(message.from_user.id)
        email = db.get_email(message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        f"Вы прошли авторизацию.\n\
        Ваше имя - {name}\n\
        Ваш факультет - {department}\n\
        Ваша почта - {email}."
    )


@dp.message_handler(lambda message: is_set_email_state(message.from_user.id))
async def set_email_message(message):
    email = message.text
    if is_correct_email(email):
        with UsersData(DB_LOCATION) as db:
            db.set_email(message.from_user.id, email)
        await bot.send_message(
            message.from_user.id,
            "Почта введена верно. В течение минуты вам на почту придет код авторизации."
        )

        keyboard = InlineKeyboardMarkup()
        change_email_button = InlineKeyboardButton(
            text="Сменить почту", callback_data="change_email")
        resend_code_button = InlineKeyboardButton(
            text="Отправить письмо заново", callback_data="resend_code")
        keyboard.add(change_email_button)
        keyboard.add(resend_code_button)

        await bot.send_message(
            message.from_user.id,
            "Введите код авторизации.",
            reply_markup=keyboard
        )

        send_auth_code(message.from_user.id)

        with UsersData(DB_LOCATION) as db:
            db.set_state(message.from_user.id, SET_CODE_AUTHORIZATION)
    else:
        await bot.send_message(
            message.from_user.id,
            "Введите корректную корпоративную почту."
        )


@dp.message_handler(lambda message: is_set_code_authorization_state(message.from_user.id))
async def set_code_authorization_email_message(message):
    code = message.text
    if is_correct_auth_code(code, message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            "Код введен верно. Перейдем к заполнению анкеты."
        )
        await bot.send_message(
            message.from_user.id,
            "Введите Ваше имя."
        )
        with UsersData(DB_LOCATION) as db:
            db.set_state(message.from_user.id, SET_USERNAME)
    else:
        await bot.send_message(
            message.from_user.id,
            "Код введен неверно. Отправьте корректный код."
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


@dp.callback_query_handler(lambda call: call.data == "change_email")
async def change_email_message(call):
    await bot.send_message(
        call.from_user.id,
        "Введите новую почту."
    )
    with UsersData(DB_LOCATION) as db:
        db.set_state(call.from_user.id, SET_EMAIL)


@dp.callback_query_handler(lambda call: call.data == "resend_code")
async def resend_code_message(call):
    send_auth_code(call.from_user.id)
    await bot.send_message(
        call.from_user.id,
        "Новый код отправлен на вашу почту."
    )


if __name__ == '__main__':
    executor.start_polling(dp)