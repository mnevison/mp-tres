from flask import Blueprint, render_template, request, flash, redirect, url_for
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
                flash("You're now logged in!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.dashboard"))
            else:
                flash("Password incorrect", category="danger")
        else:
            flash("Email not recognized", category="danger")
        return render_template("login.html", user=current_user)
    
    return render_template ("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    print("Reached the register route") # debugging
    if request.method == "POST":
        print("Form submitted") # debugging
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        print("Email:", email) # debugging
        print("First Name:", fname) # debugging
        print("Last Name:", lname) # debugging
        print("Password1:", password1) # debugging
        print("Password2:", password2) # debugging

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already registered.", category="danger")
        elif len(email) <11:
            flash("Minimum 10 characters required.", category="danger")
        elif len(fname) <2:
            flash("Name too short.", category="danger")
        elif len(lname) <2:
            flash("Name too short.", category="danger")
        elif password1 != password2:
            flash("Passwords don't match.", category="danger")
        elif len(password1) <7:
            flash("Password too short, must be at least 7 characters. ", category="danger")
        else:
            new_user = User(email=email, fname=fname, lname=lname, password=generate_password_hash(password1, method="pbkdf2:sha256"))
            db.session.add(new_user)
            print("User added to session, now committing...")
            db.session.commit()
            print("User committed to database")
            login_user(new_user, remember=True)
            flash("New Account Created!", category="success")
            return redirect(url_for("views.dashboard"))



    return render_template ("register.html")