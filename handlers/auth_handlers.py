from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from misc import dp, bot
import logic.auth_logic as auth
from utils.db_operations import UsersData
from data.states import *
from data.config import DB_LOCATION
from data.cities import cities


@dp.message_handler(lambda message: auth.is_authorized(message.from_user.id))
async def message_to_authorized_person(message):
    with UsersData(DB_LOCATION) as db:
        city = db.get_city(message.from_user.id)
        department = db.get_department(message.from_user.id)
        social_network = db.get_social_network(message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        f"Вы прошли авторизацию.\n" +
        f"Ваш город - {city}\n" + 
        f"Ваш факультет - {department}\n" +
        f"Ваша страница в социальной сети - {social_network}."
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

        keyboard = ReplyKeyboardMarkup()
        change_email_button = KeyboardButton(text="Сменить почту")
        resend_code_button = KeyboardButton(text="Отправить письмо заново")
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
    if message.text == "Сменить почту":
        await bot.send_message(
            message.from_user.id,
            "Введите новую почту."
        )
        with UsersData(DB_LOCATION) as db:
            db.set_state(message.from_user.id, SET_EMAIL)
        return
    elif message.text == 'Отправить письмо заново':
        auth.send_auth_code(message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            "Новый код отправлен на вашу почту."
        )
        return
    code = message.text
    if auth.is_correct_auth_code(code, message.from_user.id):
        await bot.send_message(
            message.from_user.id,
            "Код введен верно. Перейдем к заполнению анкеты.",
            reply_markup=ReplyKeyboardRemove(),
        )
        with UsersData(DB_LOCATION) as db:
            db.set_state(message.from_user.id, SET_CITY)
        keyboard = ReplyKeyboardMarkup()
        for city in cities:
            button = KeyboardButton(text=city)
            keyboard.add(button)
        await bot.send_message(
            message.from_user.id,
            "Выберите ваш город.",
            reply_markup=keyboard
        )
    else:
        await bot.send_message(
            message.from_user.id,
            "Код введен неверно. Отправьте корректный код."
        )


@dp.message_handler(lambda message: auth.is_set_city_state(message.from_user.id))
async def set_city_message(message):
    if message.text in cities:
        with UsersData(DB_LOCATION) as db:
            db.set_city(message.from_user.id, message.text)
            db.set_state(message.from_user.id, SET_DEPARTMENT)
            await bot.send_message(
                message.from_user.id,
                "Введите название вашего факультета",
                reply_markup=ReplyKeyboardRemove(),
            )
    else:
        await bot.send_message(
            message.from_user.id,
            "Введите корректный город.",
        )


@dp.message_handler(lambda message: auth.is_set_department_state(message.from_user.id))
async def set_department_message(message):
    with UsersData(DB_LOCATION) as db:
        db.set_department(message.from_user.id, message.text)
        db.set_state(message.from_user.id, SET_SOCIAL_NETWORK)
        await bot.send_message(
            message.from_user.id,
            "Введите ссылку на вашу страницу в социальной сети."
        )


@dp.message_handler(lambda message: auth.is_set_social_network_state(message.from_user.id))
async def set_social_network_message(message):
    with UsersData(DB_LOCATION) as db:
        db.set_social_network(message.from_user.id, message.text)
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