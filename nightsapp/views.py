from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .models import Task
from .database import db

views = Blueprint('views', __name__)

@views.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template ("dashboard.html")


@views.route("/create_task", methods=["GET"])
@login_required
def task_form():
    return render_template ("create_task.html")


@views.route("/create_task", methods=["POST"])
@login_required
def create_task():
    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    start_date = request.form["start_date"]
    due_date = request.form["due_date"]
    status = request.form["status"]

    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        start_date=start_date,
        due_date=due_date,
        status=status,
        user_id=current_user.id
    )

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for("views.dashboard"))