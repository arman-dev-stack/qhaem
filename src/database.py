from pymongo import MongoClient
from uuid import uuid4
import datetime as dt
from . import scripts

mongodb = MongoClient('127.0.0.1', 27017)

db = mongodb['qhaem']

def get_token_admin(data: dict):
    admin = db['admins'].find_one({
        'username': data['username'],
        'password': data['password'],
    })
    if admin:
        return admin['token']

def check_admin_token(admin_token):
    admin = db['admins'].find_one({
        'token': admin_token
    })
    return bool(admin)


def get_admin(admin_token):
    return db['admins'].find_one({
        'token': admin_token
    })

def get_user_information():
    ...

def show_admins_in_admin_panel():
    admins = db['admins'].find()
    return admins