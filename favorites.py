'''Module for handling all recipe faving activities: add, del, check'''
from sqlalchemy.sql import text
from db import db


def mark_recipe_as_favorite(recipe_id : int, user_id : int):
    '''To mark a recipe as a favorite > added to favorites list'''

    try:
        sql = text("""INSERT INTO favorites (user_id, recipe_id)
        VALUES (:user_id, :recipe_id)""")
        db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id})
        db.session.commit()

    except SystemError:
        return False
    return True


def cancel_set_as_favorite(recipe_id : int, user_id : int):
    '''Removes the recipe from users favorites'''

    try:
        sql = text("""DELETE FROM favorites WHERE user_id = :user_id AND recipe_id = :recipe_id""")
        db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id})
        db.session.commit()

    except SystemError:
        print("Favorite not found. Nothing has been deleted.")
        return False

    return True


def show_my_favorites(user_id):
    '''Returns list of users favorites recipes'''

    try:
        sql = text("SELECT DISTINCT " +
                   "recipes.* "+
                   "FROM favorites "+
                   "INNER JOIN recipes ON (favorites.recipe_id = recipes.id) " +
                   "WHERE favorites.user_id = :user_id")

        result = db.session.execute(sql, {"user_id":user_id})
        favorite_list = result.fetchall()

    except SystemError:
        return "Error - no favorites found"

    return favorite_list


def check_favorite_status(recipe_id, user_id):
    '''Check is logged in user has already added this recipe as their favorite.
    Returns a list that has a value in index 0: 0 or 1. 1 means True: this recipe
    already is in users favorite list. 0 means that it is not.'''

    try:
        sql = text("SELECT COUNT(*) AS favorite_status " +
                   "FROM favorites " +
                   "INNER JOIN recipes ON (favorites.recipe_id = recipes.id) " +
                   "WHERE favorites.user_id = :user_id AND favorites.recipe_id = :recipe_id")

        result = db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id})
        favorite_status_table = result.fetchone()
        favorite_status = int(favorite_status_table[0])

    except SystemError:
        return "Error - no favorites found"

    return favorite_status
