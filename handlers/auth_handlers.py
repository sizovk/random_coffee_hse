from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from misc import dp, bot
import logic.auth_logic as auth
from utils.db_operations import UsersData
from data.states import *
from data.config import DB_LOCATION


@dp.message_handler(lambda message: auth.is_authorized(message.from_user.id))
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


@dp.message_handler(lambda message: auth.is_set_email_state(message.from_user.id))
async def set_email_message(message):
    email = message.text
    if auth.is_correct_email(email):
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

        auth.send_auth_code(message.from_user.id)

        with UsersData(DB_LOCATION) as db:
            db.set_state(message.from_user.id, SET_CODE_AUTHORIZATION)
    else:
        await bot.send_message(
            message.from_user.id,
            "Введите корректную корпоративную почту."
        )


@dp.message_handler(lambda message: auth.is_set_code_authorization_state(message.from_user.id))
async def set_code_authorization_email_message(message):
    code = message.text
    if auth.is_correct_auth_code(code, message.from_user.id):
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


@dp.message_handler(lambda message: auth.is_set_username_state(message.from_user.id))
async def set_username_message(message):
    with UsersData(DB_LOCATION) as db:
        db.set_username(message.from_user.id, message.text)
    await bot.send_message(
        message.from_user.id,
        f"Введите название Вашего факультета."
    )
    with UsersData(DB_LOCATION) as db:
        db.set_state(message.from_user.id, SET_DEPARTMENT)


@dp.message_handler(lambda message: auth.is_set_department_state(message.from_user.id))
async def set_department_message(message):
    with UsersData(DB_LOCATION) as db:
        db.set_department(message.from_user.id, message.text)
    with UsersData(DB_LOCATION) as db:
        db.set_state(message.from_user.id, AUTHORIZED)
        await bot.send_message(
        message.from_user.id,
        "Авторизация завершена."
    )


@dp.message_handler(lambda message: auth.is_not_authorized(message.from_user.id))
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
    auth.send_auth_code(call.from_user.id)
    await bot.send_message(
        call.from_user.id,
        "Новый код отправлен на вашу почту."
    )