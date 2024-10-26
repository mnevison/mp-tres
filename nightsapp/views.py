# Import necessary modules and functions from Flask and Flask-Login
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required
from .models import Task
from .database import db

# Create a Blueprint for the views, allowing routes to be grouped
views = Blueprint('views', __name__)

# Dashboard route (GET): Displays a list of tasks for the logged-in user
@views.route("/dashboard", methods=["GET"])
def dashboard():
    # Retrieve all tasks associated with the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    # Render the dashboard template and pass the tasks to it
    return render_template("dashboard.html", tasks=tasks)

# Task form route (GET): Displays the form to create a new task (accessible only when logged in)
@views.route("/create_task", methods=["GET"])
@login_required
def task_form():
    # Render the create task form template
    return render_template("create_task.html")

# Task creation route (POST): Processes the form submission to create a new task (requires login)
@views.route("/create_task", methods=["POST"])
@login_required
def create_task():
    # Retrieve form data submitted by the user
    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    start_date = request.form["start_date"]
    due_date = request.form["due_date"]
    status = request.form["status"]

    # Create a new task object with the provided form data
    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        start_date=start_date,
        due_date=due_date,
        status=status,
        user_id=current_user.id  # Associate the task with the current user
    )

    # Add the new task to the database and commit the transaction
    db.session.add(new_task)
    db.session.commit()

    # Redirect the user back to the dashboard after successful task creation
    return redirect(url_for("views.dashboard"))

# Task editing route (GET/POST): Allows users to edit an existing task (requires login)
@views.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    # Retrieve the task by its ID, or return a 404 if not found
    task = Task.query.get_or_404(task_id)

    # If the form is submitted (POST), update the task's attributes
    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form["description"]
        task.priority = request.form["priority"]
        task.start_date = request.form["start_date"]
        task.due_date = request.form["due_date"]
        task.status = request.form["status"]

        # Commit the changes to the database
        db.session.commit()

        # Redirect back to the dashboard after updating the task
        return redirect(url_for("views.dashboard"))

    # Render the task editing template, passing the task data to it (GET)
    return render_template("edit_task.html", task=task)

# Task deletion route (POST): Handles task deletion (requires login)
@views.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    # Retrieve the task by its ID, or return a 404 if not found
    task = Task.query.get_or_404(task_id)

    # Delete the task from the database and commit the transaction
    db.session.delete(task)
    db.session.commit()

    # Redirect back to the dashboard after deletion
    return redirect(url_for("views.dashboard"))


# Route to get task details for the calendar modal 
@views.route("/task/<int:task_id", methods=["GET"])
@login_required
def get_tasks():
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        abort(403)
    
    return jsonify({

        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "start_date": task.start_date.strftime('%Y-%m-%dT%H:%M'),
        "end_date": task.end_date.strftime('%Y-%m-%dT%H:%M'),
        "status": task.status
    })
