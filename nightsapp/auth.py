from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Welcome back, {}!".format(user.fname), category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.dashboard"))
            else:
                flash("Email or Password incorrect", category="danger")
        
            return render_template("login.html", email=email)
            
        return render_template("login.html", user=current_user)
    
    return render_template ("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Perform validation checks
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already registered.", category="danger")
        elif len(email) < 11:
            flash("Email must be at least 11 characters long.", category="danger")
        elif len(fname) < 2:
            flash("First name is too short.", category="danger")
        elif len(lname) < 2:
            flash("Last name is too short.", category="danger")
        elif password1 != password2:
            flash("Passwords don't match.", category="danger")
        elif len(password1) < 7:
            flash("Password too short, must be at least 7 characters.", category="danger")
        else:
            # Create and add the new user to the database
            new_user = User(email=email, fname=fname, lname=lname, password=generate_password_hash(password1, method="pbkdf2:sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("New Account Created!", category="success")
            return redirect(url_for("views.dashboard"))

        # If validation fails, pass the form data back to the template
        return render_template("register.html", email=email, fname=fname, lname=lname)

    # Render the registration page for a GET request
    return render_template("register.html")

@auth.route("/logout")
def logout():
    logout_user()
    flash("You've been successfully logged out", category="success")
    return redirect(url_for("auth.login"))