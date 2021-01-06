from utils.db_operations import UsersData
from data.states import *
from data.config import DB_LOCATION
from random import randint
import smtplib


def is_before_meeting(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == BEFORE_MEETING


def is_accept_meeting(chat_id):
    with UsersData(DB_LOCATION) as db:
        return db.get_state(chat_id) == ACCEPT_MEETING