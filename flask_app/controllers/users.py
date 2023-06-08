from flask_app import app
from flask import render_template, redirect, session, url_for, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
from flask_app.controllers import recipes
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if not user.User.is_valid(request.form):
        return redirect(url_for("home"))
    if not user.User.check_email(data = {"email": request.form["email"]}): 
        return redirect(url_for("home"))
    else:
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form["password"])
        }
        
        user.User.create(data)
        session["email"] = request.form["email"]
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        return redirect(url_for("all_recipes"))

@app.route("/login", methods=["POST"])
def login():
    data = {
        "email": request.form["email"]
    }
    user_from_db = user.User.get_user_by_email(data)
    if not user_from_db:
        flash("Invalid Login")
        return redirect(url_for("home"))
    if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        flash("Invalid Login")
        return redirect(url_for('home'))
    session["first_name"] = user_from_db.first_name
    session["last_name"] = user_from_db.last_name
    session["email"] = request.form["email"]
    session['logged_in'] = user_from_db.id
    return redirect(url_for("all_recipes"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))