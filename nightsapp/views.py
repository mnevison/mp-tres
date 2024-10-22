from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .models import Task
from .database import db

views = Blueprint('views', __name__)

@views.route("/dashboard", methods=["GET"])
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", tasks=tasks)


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

@views.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form["description"]
        task.priority = request.form["priority"]
        task.start_date = request.form["start_date"]
        task.due_date = request.form["due_date"]
        task.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("views.dashboard"))


    return render_template("edit_task.html", task=task)

@views.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("views.dashboard"))