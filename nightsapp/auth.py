from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("/")
def login():
    return render_template ("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already registered.", category="error")
        elif len(email) <11:
            flash("Minimum 10 characters required.", category="error")
        elif len(fname) <2:
            flash("Name too short.", category="error")
        elif len(lname) <2:
            flash("Name too short.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) <7:
            flash("Password too short, must be at least 7 characters. ", category="error")
        else:
            new_user = User(email=email, fname=fname, lname=lname, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("New Account Created!", category="success")
            return redirect(url_for("views.calendar"))



    return render_template ("register.html")