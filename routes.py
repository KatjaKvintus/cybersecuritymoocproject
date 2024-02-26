'''Module for handling page requests'''
from random import randint
from flask import redirect, render_template, request, session, abort
#from django.views.decorators.csrf import csrf_exempt
from app import app
import stars
import users
import recipes
import comments
import favorites
import secrets



@app.route("/", methods=["GET", "POST"])
def index():
    '''Route: index.html'''
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    '''Handles login function'''

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    if not users.username_taken(username):
        return render_template("error.html", message="this username does not exist.")

    # Check if the username exists and matches with the password
    if not users.log_in_user(username, password):
        return render_template("error.html", message="incorrect username or password")
    
    session["csrf_token"] = secrets.token_hex(16)

    return redirect("/mainpage")


@app.route("/register", methods=["GET", "POST"])
def register():
    '''Creating a new user account for both users and admins'''

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        user_type = request.form["user_type"]
        admin_key = request.form["admin_key"]

    correct_admin_key = users.get_admin_key()

    if user_type == "admin" and admin_key != correct_admin_key:
        return render_template("error.html",
                                message="Incorrect admin key. Please check the spelling.")

    if len(username) < 3:
        return render_template("error.html",
                                message="Too short username. " +
                                "Please choose one that has at least 3 characters.")

    if len(username) > 20:
        return render_template("error.html",
                                message="This username is too long. " +
                                "Please choose one that has maximum 20 characters.")

    if users.username_taken(username):
        return render_template("error.html",
                                message="This username is taken. Please choose another one.")

    if password1 != password2:
        return render_template("error.html",
                                message="Passwords don't match. " +
                               "Please type the sama password twice.")

    if len(password1) < 3:
        return render_template("error.html",
                                message="This password is too short. " +
                               "Please choose one that has at least 3 characters.")

    if not users.create_new_account(username, password1, user_type):
        return render_template("error.html",
                                message="Failed to create the user account.")

    return redirect("/mainpage")


@app.route("/mainpage", methods=["GET", "POST"])
def mainpage():
    '''Handles data neede for setting up the app main page and it's links'''

    try:
        latest_recipe = recipes.show_latest_recipe()

        try:
            index_for_recipe_of_the_week = recipes.get_index_for_the_latest_recipe_of_the_week()
        except SystemError:
            index_for_recipe_of_the_week=index_for_recipe_of_the_week = 0
        return render_template("mainpage.html", latest_recipe=latest_recipe,
                                 index_for_recipe_of_the_week=index_for_recipe_of_the_week)

    except SystemError:
        print("No entries in the database.")
        latest_recipe = [0]
        return render_template("mainpage.html", latest_recipe=latest_recipe,
                                 index_for_recipe_of_the_week=index_for_recipe_of_the_week,
                                 csrf_token=session.csrf_token)


@app.route("/search")
def search():
    '''Search function'''
    return render_template("search.html")


@app.route("/search_function", methods=["GET", "POST"])
def search_function():
    '''All search functionalities: name, type and keyword'''

    query1 = request.args["query1"]
    query2 = request.args["query2"]

    if query1 != None:
        list_of_search_matching_recipes = recipes.search_recipe_by_name(query1)
    elif query2 != None:
        list_of_search_matching_recipes = recipes.search_recipe_by_name(query2)

    recipe_amount = len(list_of_search_matching_recipes)

    return render_template("search_results.html", recipe_amount=recipe_amount,
                            list_of_search_matching_recipes=list_of_search_matching_recipes)


@app.route("/search_results", methods=["GET", "POST"])
def search_results():
    '''Handling search results listing'''

    source_route = source_route
    return render_template("search_results.html", source_route=source_route)


@app.route("/page", methods=["GET", "POST"])
def page():
    '''Displays individual recipe based in the id number, including comments, reviews
    and function to set the recipe as favorite'''

    user_id = users.get_user_id()

    if request.method == "POST":
        
        recipe_id = request.form["this_is_recipe_id"]

        if recipe_id != "":
            show_this_recipe = recipes.collect_recipe_items(recipe_id)
            recipe_comments = comments.show_comments(recipe_id)
            star_rating = stars.count_stars(recipe_id)
            recipe_fav_status = favorites.check_favorite_status(recipe_id, user_id)
            recipe_stars_status = stars.check_if_user_has_given_stars(recipe_id, user_id)
        else:
            return render_template("error.html",
                                message="The database is empty. " +
                                "Maybe you can be the author of our first recipe?")

    if len(recipe_comments) == 0:
        note = "No comments yet. Be the first one?"
    else:
        note = "Comments for this recipe: " + str(len(recipe_comments)) + " pcs"

    if star_rating[0] == 0:
        rating_text = "No reviews yet. Be the first one?"
    else:
        rating_text = "Reviews for this recipe: " + str(star_rating[0]) + "/5 from "
        rating_text = rating_text + str(star_rating[1]) + " reviewers"

    if recipe_stars_status == 1:
        recipe_stars_status = "You have already reviewed this recipe."
    else:
        recipe_stars_status = "You have not yet reviewed this recipe."

    if recipe_fav_status == 1:
        recipe_fav_status = "This recipe is already in your favorites."
    else:
        recipe_fav_status = "This recipe is not yet in your favorites."

    return render_template("recipe.html", recipe_id=recipe_id, show_this_recipe=show_this_recipe,
                             recipe_comments=recipe_comments, note=note,
                             rating_text=rating_text,
                             recipe_fav_status=recipe_fav_status,
                             recipe_stars_status=recipe_stars_status)


@app.route("/recipe_type", methods=["GET", "POST"])
def type():
    '''Search functionality for searching recipes by type'''

    type = request.form["type"]
    if type != None:
        list_of_search_matching_recipes = recipes.list_recipes_by_type(type)
        recipe_amount = len(list_of_search_matching_recipes)

    source_route = "Recipes by type"

    return render_template("search_results.html", recipe_amount=recipe_amount,
                            list_of_search_matching_recipes=list_of_search_matching_recipes,
                            source_route=source_route)


@app.route("/all_recipes", methods=["GET", "POST"])
def all_recipes():
    '''Listing of all recipes in the database'''

    list_of_search_matching_recipes = recipes.get_all_recipes()
    recipe_amount = len(list_of_search_matching_recipes)

    source_route = "All recipes"

    return render_template("search_results.html", recipe_amount=recipe_amount,
                            list_of_search_matching_recipes=list_of_search_matching_recipes,
                            source_route=source_route)


@app.route("/add_new_recipe", methods=["GET", "POST"])
def add_new_recipe():
    '''Adding new recipe to the database'''

    if request.method == "GET":
        return render_template("add_new_recipe.html")

    if request.method == "POST":
        name = request.form["title"]
        type = request.form["type"]
        author_id = users.get_user_id()
        base_liquid = request.form["base_liquid"]
        grain = request.form["grain"]
        protein = request.form["protein"]
        ingredient_1 = request.form["ingredient_1"]
        ingredient_2 = request.form["ingredient_2"]
        sweetener = request.form["sweetener"]

    list_of_current_recipe_names = recipes.fetch_recipe_names()

    if name in list_of_current_recipe_names:
        return render_template("error.html",
                                message="This recipa name is already in the database. " +
                                "Please choose another name for your recipe. ")

    if len(name) > 40:
        return render_template("error.html",
                                message="Recipe name is too long. " +
                               "Please choose one that has maximum 40 characters.")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    result = recipes.save_new_recipe(name, type, author_id, base_liquid, grain,
                                      protein, ingredient_1, ingredient_2, sweetener)

    if not result:
        return render_template("error.html", message="Failed to save database.")

    return render_template("recipe_saved.html")


@app.route("/add_favorite", methods=["GET", "POST"])
def add_favorite():
    '''Adding the recipe as user's favorite one'''

    user_id = users.get_user_id()

    if request.method == "POST":
        recipe_id = request.form["favorite"]
        recipe_id = int(recipe_id)

    if favorites.mark_recipe_as_favorite(recipe_id, user_id):
        return render_template("succesfull_message.html",
                                message="Favorite saved! " +
                               "(Click back button on your browser to return to the recipe.)")

    else:
        return render_template("error.html", message="Not succesfull")


@app.route("/my_favorites", methods=["GET", "POST"])
def my_favorites():
    '''Listing of logged in users favorites recipes'''

    user_id = users.get_user_id()
    list_of_search_matching_recipes = favorites.show_my_favorites(user_id)
    recipe_amount = len(list_of_search_matching_recipes)
    source_route = "My favorites"

    return render_template("search_results.html",
                            recipe_amount=recipe_amount,
                            list_of_search_matching_recipes=list_of_search_matching_recipes,
                            source_route=source_route)


@app.route("/add_comment", methods=["GET", "POST"])
def add_comment():
    '''Adding a new comment to an individual recipe'''

    user_id = users.get_user_id()

    if request.method == "POST":
        new_comment = request.form["new_comment"]
        recipe_id = request.form["recipe_id"]

    if len(new_comment) > 1000:
        return render_template("error.html",
                                message="Your comment is too long. " +
                               "Please shorten it to maximum 1000 characters.")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    result = comments.add_comment(user_id, recipe_id, new_comment)

    if not result:
        return render_template("error.html", message="Failed to add comment")
    else:
        return render_template("comment_saved.html")


@app.route("/random")
def random():
    '''Generating a random recipe for adventorous users'''

    amount_of_recipes = len(recipes.get_all_recipes())
    id = randint(1, amount_of_recipes)
    show_this_recipe = recipes.collect_recipe_items(id)
    recipe_comments = comments.show_comments(id)

    if len(recipe_comments) == 0:
        note = "No comments yet. Be the first one?"
    else:
        note = "Comments for this recipe: " + str(len(recipe_comments)) + " pcs"

    return render_template("recipe.html", id=id,
                            show_this_recipe=show_this_recipe,
                            recipe_comments=recipe_comments, note=note)


@app.route("/admin_tools", methods=["POST"])
def admin_tools():
    '''Functionalities for only admin level users'''

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
            
    if request.method == "POST":

        '''
        # Fix for flaw 3: checking the user level
        if not users.check_if_loggend_in_user_is_admin():
            return render_template("error.html", message="This section is only for admins.")
        '''
        return render_template("admin_tools.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    '''Logging out and closing sessions'''
    users.log_out()
    return render_template("logout.html")


@app.route("/check_all_recipes", methods=["POST"])
def check_all_recipes():
    '''Provides recipe listing for admins to choose one as the recipe of the week'''

    '''
    # Fix for flaw 3: checking the user level
    if not users.check_if_loggend_in_user_is_admin():
        abort(403)
    '''

    if request.method == "POST":

        recipe_list = recipes.get_all_recipes()
        largest_recipe_id = recipes.max_id_in_recipes_table

        return render_template("recipe_of_the_week.html",
                            recipe_list=recipe_list, largest_recipe_id=largest_recipe_id)


@app.route("/set_recipe_of_the_week", methods=["GET", "POST"])
def recipe_of_the_week():
    '''Setting the recipe of the week (for admins only)'''

    '''
    # Fix for flaw 3: checking the user level
    if not users.check_if_loggend_in_user_is_admin():
        abort(403)
    '''

    if request.form["recipe_id"] == 0:
        return render_template("error.html",
                                message="No recipes available.")

    if request.method == "POST":
        recipe_id = request.form["recipe_id"]
        recipes.set_recipe_of_the_week(recipe_id)

        return render_template("succesfull_message.html",
                            message="New recipe of the week published.")


@app.route("/review", methods=["GET", "POST"])
def review():
    '''Giving a star review for an individual recipe'''

    this_user_id = users.get_user_id()

    if request.method == "POST":
        this_stars = int(request.form["stars"])
        this_recipe_id = int(request.form["recipe_id"])

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    stars.give_stars(this_user_id, this_recipe_id, this_stars)

    return render_template("succesfull_message.html",
                            message="Star rating saved!")


@app.route("/delete_comment", methods=["GET", "POST"])
def delete_comment():
    '''For admin level users to delete comments from recipes'''

    if request.method == "POST":
        role = request.form["role"]
        del_comment_id = request.form["del_comment_id"]

    if role == "admin":
        comments.delete_comment(del_comment_id)
        return "Comment delete successfull"


@app.route("/change_fav_status", methods=["GET", "POST"])
def change_fav_status():
    '''For toggling favorite status on a recipe (off/off)'''

    user_id = users.get_user_id()

    if request.method == "POST":
        recipe_id = request.form["recipe_id"]

    current_status = int(favorites.check_favorite_status(recipe_id, user_id))

    if current_status == 1:
        favorites.cancel_set_as_favorite(recipe_id, user_id)
    else:
        favorites.mark_recipe_as_favorite(recipe_id, user_id)

    return redirect("/my_favorites")


@app.route("/create_new_admin", methods=["GET", "POST"])
def create_new_admin():
    '''Admin can create a new admin user account'''

    if not users.check_if_loggend_in_user_is_admin():
        abort(403)

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        user_type = "admin"

    if len(username) < 3:
        return render_template("error.html",
                                message="Too short username. " +
                                "Please choose one that has at least 3 characters.")

    if len(username) > 20:
        return render_template("error.html",
                                message="This username is too long. " +
                                "Please choose one that has maximum 20 characters.")

    if users.username_taken(username):
        return render_template("error.html",
                                message="This username is taken. Please choose another one.")

    if password1 != password2:
        return render_template("error.html",
                                message="Passwords don't match. " +
                               "Please type the sama password twice.")

    if len(password1) < 3:
        return render_template("error.html",
                                message="This password is too short. " +
                               "Please choose one that has at least 3 characters.")

    if not users.create_new_admin(username, password1):
        return render_template("error.html",
                                message="Failed to create the user account.")

    return render_template("succesfull_message.html",
                            message="New admin created! Remember to send them their new username and password.")
