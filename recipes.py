'''Module for handling all recipe relates transactions'''
from datetime import date
from sqlalchemy.sql import text
from db import db


def save_new_recipe(name, type, author_id, base_liquid, grain, protein,
                     ingredient_1, ingredient_2, sweetener):
    '''Saves new recipe to the database'''

    try:
        sql = text("""INSERT INTO recipes (name, type, author_id, base_liquid, grain,
                 protein, ingredient_1, ingredient_2, sweetener)
                 VALUES (:name, :type, :author_id, :base_liquid, :grain,
                 :protein, :ingredient_1, :ingredient_2, :sweetener)""")

        db.session.execute(sql, {"name":name, "type":type, "author_id":author_id,
                                  "base_liquid":base_liquid, "grain":grain, "protein":protein,
                                  "ingredient_1":ingredient_1, "ingredient_2":ingredient_2,
                                  "sweetener":sweetener})
        db.session.commit()

    except SystemError:
        return False

    return True


def get_all_recipes():
    '''Returns a list of all recipes in the database'''

    sql = text("SELECT * FROM recipes")
    result = db.session.execute(sql)
    recipe_list = result.fetchall()
    return recipe_list


def collect_recipe_items(id):
    '''Returns a list of individual recipe items'''

    sql = text("SELECT * FROM recipes WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    recipe_items = result.fetchone()
    return recipe_items


def show_latest_recipe():
    '''Collects idividual items from the newest recipe.
    Returns -1 if the database is empty.'''

    sql = text("SELECT MAX(id) AS latest_recipe_id FROM recipes") 
    result = db.session.execute(sql, {"id":id})
    recipe_id_latest = result.fetchone()

    if recipe_id_latest is None:
        return -1

    return recipe_id_latest


def search_recipe_by_name(keyword):
    '''Recipe search from recipe names'''

    keyword = keyword.lower()
    sql = text("SELECT * FROM recipes WHERE LOWER(name) LIKE :keyword")
    result = db.session.execute(sql, {"keyword":"%"+keyword+"%"})
    recipes = result.fetchall()
    return recipes


def search_from_ingredients(keyword):
    '''Recipe search based on ingredient'''

    keyword = keyword.lower()
    sql = text("SELECT * FROM recipes WHERE LOWER(base_liquid) LIKE :keyword " +
               "OR LOWER(grain) LIKE :keyword " +
               "OR LOWER(protein) LIKE :keyword " +
               "OR LOWER(ingredient_1) LIKE :keyword " +
               "OR LOWER(ingredient_2) LIKE :keyword " +
               "OR LOWER(sweetener) LIKE :keyword")
    result = db.session.execute(sql, {"keyword":"%"+keyword+"%"})
    recipes = result.fetchall()
    return recipes


def list_recipes_by_type(type):
    '''Recipe listing by type'''

    type = type.lower()
    sql = text("SELECT * FROM recipes WHERE LOWER(type) LIKE :type")
    result = db.session.execute(sql, {"type":"%"+type+"%"})
    recipes = result.fetchall()
    return recipes


def set_recipe_of_the_week(recipe_id):
    '''Admin function: one of the database recipes can be set
    as the recipe of the week'''


    this_date = str(date.today())

    try:
        sql = text("""INSERT INTO recipe_of_the_week (recipe_id, date)
                 VALUES (:recipe_id, :date)""")

        db.session.execute(sql, {"recipe_id":recipe_id, "date":this_date})
        db.session.commit()

    except SystemError:
        return False

    return True


def get_index_for_the_latest_recipe_of_the_week():
    '''Checks recipe_of_the_week tables lastest entry
    and returns the id of that recipe in recipes table'''

    sql = text("SELECT max(id) AS id FROM recipe_of_the_week")
    result = db.session.execute(sql)
    this_recipe = result.fetchone()
    this_recipe_id = this_recipe[0]

    try:

        sql = text("SELECT DISTINCT recipes.* " +
                    "FROM recipe_of_the_week " +
                    "INNER JOIN recipes ON (recipe_of_the_week.recipe_id = recipes.id) " +
                    "WHERE recipe_of_the_week.id = :this_recipe_id")

        result = db.session.execute(sql, {"this_recipe_id":this_recipe_id})
        recipe = result.fetchone()

        # This handles the case when there is no 'recipe of the week' published yet
        if recipe == None:
            recipe = [0]

    except SystemError:
        print("No recipes of the week available")

    if len(recipe) == 0:
        return 0
    else:
        index_of_the_latest_one = recipe[0]
        return index_of_the_latest_one


def fetch_recipe_names():
    '''Returns a list of recipe names already in the database
    to prevent users adding multiple recipes in the same name'''

    recipe_list = get_all_recipes()
    recipe_names = []

    for item in recipe_list:
        recipe_names.append(item[1])

    return recipe_names


def max_id_in_recipes_table():
    '''Returns the largest id in the recipes table'''

    sql = text("SELECT MAX(id) as max_id FROM recipes")
    result = db.session.execute(sql)
    max_id = result.fetchall()

    if len(max_id) < 1 or not max_id:
        return 0
    else:
        return max_id[0]
