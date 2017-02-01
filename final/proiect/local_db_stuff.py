"""Local database actions

"""
import collections
import json

from local_db_init import session
from local_db_init import User


class DBStuff:
    def __init__(self):
        pass

    @staticmethod
    def add_user(username, password, birthday, gender, country):
        user = User(username=username)
        user.password = password
        user.birthday = birthday
        user.gender = gender
        user.country = country

        session.add(user)
        session.commit()

    @staticmethod
    def get_user(username):
        user = session.query("User").filter_by(username=username).first()
        if not user:
            return False
        else:
            return True
