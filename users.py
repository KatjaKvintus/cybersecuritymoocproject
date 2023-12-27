'''All user related functions'''
import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db


# This key is needed when creating an admin level user account
ADMIN_KEY = "YouCantGuessTh1$"

def get_admin_key():
    '''Returns the admin key needed for creating an admin account'''
    return "YouCantGuessTh1$"


def get_user_id():
    '''return the user id for logged in user'''
    return session.get("user_id", 0)


def log_in_user(name, password):
    '''Log in function for users that have an user account'''

    sql = text("SELECT id, password, role FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()

    if not user:
        return False

    if not check_password_hash(user[1], password):
        return False

    session["user_id"] = user[0]
    session["user_name"] = name
    session["user_role"] = user[2]
    session["csrf_token"] = secrets.token_hex(16)

    return True


def create_new_account(name, password, user_type):
    '''Creates new user account and directs to login'''

    hash_value = generate_password_hash(password)
    role = user_type

    try:
        sql = "INSERT INTO users (name, password, role) VALUES (" + name + ", " + password + ", " + role + ")"
        db.session.execute(sql)
        db.session.commit()

    except SystemError:
        return False

    return log_in_user(name, password)


def username_taken(username):
    '''Checks if suggested username is already in use.
    Returns false if this username is unique.'''

    sql = text("SELECT name FROM users WHERE name=:username")
    result = db.session.execute(sql, {"username":username})
    list_of_usernames = result.fetchall()
    answer = len(list_of_usernames)

    if answer == 0:
        return False
    else:
        return True


def log_out():
    '''Logging out of app and closing all active sessions'''

    del session["user_id"]
    del session["user_name"]
