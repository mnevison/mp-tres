# Import necessary modules and functions from Flask and Flask-Login
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Task, Holiday
from .database import db
from datetime import datetime
import os

# Create a Blueprint for the views, allowing routes to be grouped
views = Blueprint('views', __name__)

# Dashboard route (GET): Displays a list of tasks for the logged-in user
@views.route("/dashboard", methods=["GET"])
def dashboard():
    # Retrieve all tasks associated with the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    holidays = Holiday.query.all()

    holiday_events = [
        {
            'title': f"{holiday.owner.fname} {holiday.owner.lname} - {'Approved' if holiday.is_approved else 'Declined' if holiday.is_declined else 'Pending'}",
            'start': holiday.start_date.isoformat(),
            'end': holiday.end_date.isoformat(),
            'allDay': True,
            'color': (
                'green' if holiday.is_approved else
                'red' if holiday.is_declined else
                'orange' #if pending
                )
        }
        for holiday in holidays
    ]

    task_events = [
        {
            'title': task.title,
            'start': task.start_date.isoformat() if task.start_date else datetime.now().isoformat(),
            'end': task.due_date.isoformat() if task.due_date else datetime.now().isoformat(),
        }
        for task in tasks
    ]
    # Render the dashboard template and pass the tasks to it    
    return render_template("dashboard.html", tasks=tasks, holidays=holidays, holiday_events=holiday_events, task_events=task_events)

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

    if request.method == "POST":

        # Retrieve form data submitted by the user
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        start_date = request.form["start_date"]
        due_date = request.form["due_date"]
        status = request.form["status"]

        # convert to string for comparison 
        start_date_str = datetime.strftime(start_date, "%Y-%m-%d")
        due_date_str = datetime.strftime(due_date, "%Y-%m-%d")

        # validation that due is not before start date
        if due_date_str < start_date_str:
            flash("Due date cannot be before the start date.", "danger")
            return render_template("create_task.html", title=title, description=description, priority=priority, start_date=start_date, due_date=due_date, status=status)

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

    # If request = GET, render empty create_task form
    return render_template("create_task.html")

# Task editing route (GET/POST): Allows users to edit an existing task (requires login)
@views.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    # Retrieve the task by its ID, or return a 404 if not found
    task = Task.query.get_or_404(task_id)

    # If the form is submitted (POST), update the task's attributes
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        start_date_str = request.form["start_date"]
        due_date_str = request.form["due_date"]
        status = request.form["status"]

        # converts str into datetime objects
        try:
            start_date= datetime.fromisoformat(start_date_str)
            due_date= datetime.fromisoformat(due_date)
        except ValueError:
            flash("Invalid date format.", "danger")
            return render_template("edit_task.html", task=task)
        # validates due date isn't before start date
        if due_date < start_date:
            flash("Due date cannot be before the start date.")
            return render_template("edit_task.html", task=task)

        task.title = title
        task.description = description
        task.priority = priority
        task.start_date = start_date
        task.due_date = due_date
        task.status = status

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


@views.route("/request_holiday", methods=["GET", "POST"])
@login_required
def request_holiday():
    if request.method == "POST":
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")

        try:
            # Ensure that both start_date_str and end_date_str are provided
            if not start_date_str or not end_date_str:
                flash("Start date and end date are required.", "danger")
                return render_template("request_holiday.html")

            # Parse the dates from the provided strings
            start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")

            # Validate that the start date is before the end date
            if start_date >= end_date:
                flash("Start date must be before end date.", "danger")
                return render_template("request_holiday.html")

            # Create a new holiday request
            new_holiday = Holiday(
                start_date=start_date,
                end_date=end_date,
                is_approved=False, # Initial state is unapproved
                user_id=current_user.id
            )

            # Add the new holiday to the database and commit
            db.session.add(new_holiday)
            db.session.commit()

            flash("Holiday request submitted! Please await approval from admin.", "success")
            return redirect(url_for("views.dashboard"))

        except ValueError:
            flash("Invalid date format. Please use the correct format.", "danger")
            return redirect(url_for("views.request_holiday"))

    return render_template("request_holiday.html")


@views.route("/edit_holiday/<int:holiday_id>", methods=["GET", "POST"])
@login_required
def edit_holiday(holiday_id):
    holiday = Holiday.query.get_or_404(holiday_id)

    if not current_user.is_admin and holiday.user_id != current_user.id:
        flash("You are not authorized to edit this holiday request", "danger")
        return redirect(url_for("views.dashboard"))

    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
                
        if not start_date or not end_date:
            flash("Start date and end date are required.", "danger")
            return render_template("edit_holiday.html", holiday=holiday)

        if start_date >= end_date:
            flash("Start date must be before end date.", "danger")
            return render_template("edit_holiday.html", holiday=holiday)

        holiday.start_date = start_date
        holiday.end_date = end_date

        #reset approval back to pending when editing a holiday request, unless already pending
        holiday.is_approved = False
        holiday.is_declined = False

        flash("Request Updated and sent for approval!", "success")
        
        db.session.commit()
        return redirect(url_for("views.dashboard"))

    return render_template("edit_holiday.html", holiday=holiday)


@views.route("/delete_holiday/<int:holiday_id>", methods=["POST"])
@login_required
def delete_holiday(holiday_id):
    # Retrieve the holiday by its ID, or return a 404 if not found
    holiday = Holiday.query.get_or_404(holiday_id)

    if not current_user.is_admin and holiday.user_id != current_user.id:
        flash("You are not authorized to delete this holiday request.", "danger")
        return redirect(url_for("views.dashboard"))

    # Delete the holiday from the database and commit the transaction
    db.session.delete(holiday)
    db.session.commit()
    flash("Holiday request deleted successfully!", "success")
    # Redirect back to the dashboard after deletion
    return redirect(url_for("views.dashboard"))

@views.route("/approve_holiday", methods=["GET", "POST"])
@login_required
def approve_holiday():
    if request.method == "POST":
        unapproved_holidays = Holiday.query.filter_by(is_approved=False, is_declined=False).all()

        for holiday in unapproved_holidays:
            holiday_action = request.form.get(f'holiday_action_{holiday.id}')
            if holiday_action == 'approve':
                holiday.is_approved = True
                holiday.is_declined = False 
            elif holiday_action == 'decline':
                holiday.is_approved = False
                holiday.is_declined = True 

            db.session.commit()

        flash("Holiday requests updated successfully.", "success")
        return redirect(url_for("views.dashboard"))

    unapproved_holidays = Holiday.query.filter_by(is_approved=False, is_declined=False).all()
    return render_template("approve_holiday.html", holidays=unapproved_holidays)


    


