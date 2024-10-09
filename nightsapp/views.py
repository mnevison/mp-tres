from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route("/calendar")
def calendar():
    return render_template ("calendar.html")