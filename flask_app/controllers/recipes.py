from flask import render_template, redirect, request, url_for, session, flash
from flask_app import app
from flask_app.models import recipe


@app.route("/recipes")
def all_recipes():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("home"))
    else:
        all_recipes = recipe.Recipe.get_all_recipes_with_users()
        return render_template("all_recipes.html", recipes = all_recipes)

@app.route("/recipes/new")
def create_recipe():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("home"))
    else:
        return render_template("new_recipes.html")

@app.route('/recipes/process', methods=['POST'])
def process_recipe():
    if not recipe.Recipe.is_valid(request.form):
        return redirect(url_for("create_recipe"))
    else:
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "cooked_at": request.form["cooked"],
            "under_30": request.form["under_30"],
            "user_id": request.form["user_id"]
        }
        recipe.Recipe.create_recipe(data)
        return redirect('/recipes')

@app.route('/recipes/update/<int:id>')
def update(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("home"))
    else:
        one_recipe = recipe.Recipe.get_one_with_user({"id": id})
        return render_template("edit_recipe.html", one_recipe = one_recipe)

@app.route('/recipes/update/process', methods=['POST'])
def update_process():
    if not recipe.Recipe.is_valid(request.form):
        return redirect(url_for("create_recipe"))
    else:
        data = {
            "id": request.form["recipe_id"],
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "cooked_at": request.form["cooked"],
            "under_30": request.form["under_30"],
            "user_id": request.form["user_id"]
        }

        recipe.Recipe.update(data)
        return redirect( url_for("all_recipes", id = request.form["user_id"]))

@app.route("/recipes/<int:id>")
def one_recipe(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("home"))
    else:
        user_id = int(session["logged_in"])
        recipe_from_db = recipe.Recipe.get_one_with_user({"id": id})
        return render_template("one_recipe.html", one_recipe = recipe_from_db, user_id = user_id)

@app.route("/recipes/delete/<int:id>")
def delete(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("home"))
    else:
        recipe.Recipe.delete_recipe({"id": id})
        return redirect (url_for("all_recipes"))