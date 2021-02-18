from utils.db_operations import UsersData
from data.states import *
from data.config import DB_LOCATION
from random import randint
import smtplib


def is_authorized(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == AUTHORIZED


def is_set_email_state(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == SET_EMAIL


def is_set_code_authorization_state(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == SET_CODE_AUTHORIZATION

def is_set_city_state(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == SET_CITY

def is_set_department_state(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == SET_DEPARTMENT

def is_set_social_network_state(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == SET_SOCIAL_NETWORK

def is_not_authorized(chat_id):
    with UsersData(DB_LOCATION) as db:
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
        email = db.get_email(chat_id)
    if email == "test@hse.ru":
        auth_code = '0000'
    with UsersData(DB_LOCATION) as db:
        db.set_auth_code(chat_id, auth_code)
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