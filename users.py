'''All user related functions'''
import secrets
from flask import session
#from werkzeug.security import check_password_hash, generate_password_hash
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
    

    #if not check_password_hash(user[1], password):
    if not check_username_and_password_match(name, password):
        return False

    session["user_id"] = user[0]
    session["user_name"] = name
    session["user_role"] = user[2]
    session["csrf_token"] = secrets.token_hex(16)

    return True


def create_new_account(name, password, user_type):
    '''Creates new user account and directs to login'''

    role = user_type

    try:

        sql = text("INSERT INTO users (name, password, role) VALUES ('" + name + "', '" + password + "', '" + role + "')")

        db.session.execute(sql)       
        db.session.commit()

    except SystemError:
        return False

    ''' # Fix to flaw 1
    role = user_type
    hash_value = generate_password_hash(password)

    try:

        sql = text("""INSERT INTO users (name, password, role)
                 VALUES (:name, :password, :role)""")

        db.session.execute(sql, {"name":name, "password":hash_value, "role":role})       
        db.session.commit()
        

    except SystemError:
        return False
    
        '''

    return log_in_user(name, password)


def create_new_admin(name, password):
    '''Creates new user account and directs to login'''

    role = "admin"

    try:

        sql = text("INSERT INTO users (name, password, role) VALUES ('" + name + "', '" + password + "', '" + role + "')")

        db.session.execute(sql)       
        db.session.commit()

    except SystemError:
        return False

    ''' # Another method to fix the flaw 1
    role = user_type
    hash_value = generate_password_hash(password)

    try:

        sql = text("""INSERT INTO users (name, password, role)
                 VALUES (:name, :password, :role)""")

        db.session.execute(sql, {"name":name, "password":hash_value, "role":role})       
        db.session.commit()
        

    except SystemError:
        return False
    
        '''

    return True


def check_username_and_password_match(username, password):
    '''Returns True is given password and username matches'''

    sql = text("SELECT name, password FROM users WHERE name=:username and password=:password")
    result = db.session.execute(sql, {"username":username, "password":password})
    list_of_users = result.fetchall()

    if len(list_of_users) < 1:
        return False
    else:
        return True


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
    del session["csrf_token"]


def get_session_user_role():
    '''return the user role for logged in user'''
    return session.get("user_role", 0)


def get_user_role_from_db():
    '''Takes logged in users username and returns userrole
    that is saved to the database for that username.'''

    try:
        name = session["username"]
        sql = text ("""SELECT role FROM users WHERE name=:name""") 
        result = db.session.execute(sql, {"name":name})
        this_role = result.fetchone()
        return str(this_role[0])
        
    except SystemError:
        return 0


# Fix for flaw 3: checking the user level
#def check_if_loggend_in_user_is_admin():
    
    '''Checks if the currently logged in user is admin. Returns
    True if is, False if not'''

    '''
    if get_session_user_role() != "admin":
        return False
    elif session["user_role"] != "admin":
        return False
    elif get_user_role_from_db() != "admin":
        return False
    elif get_session_user_role() == "":
        return False
    elif not session.get("user_id"):
        return False
    else:
        return True
    '''
