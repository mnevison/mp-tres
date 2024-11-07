# Import necessary modules and functions from Flask and Flask-Login
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Task, Holiday
from .database import db
from datetime import datetime
from math import ceil

# Create a Blueprint for the views, allowing routes to be grouped
views = Blueprint('views', __name__)


# Dashboard route (GET): Displays a list of tasks for the logged-in user
@views.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    # Retrieve all holiday requests from the database
    holidays = Holiday.query.all()

    holiday_events = []  # List to store formatted holiday events for the calendar
    for holiday in holidays:
        # Determine the status and color based on approval status
        status = (
            'Approved' if holiday.is_approved else
            'Declined' if holiday.is_declined else 'Pending'
        )
        color = (
            'green' if holiday.is_approved else
            'red' if holiday.is_declined else 'orange'
        )
        holiday_events.append({
            'title': f"{holiday.owner.fname} {holiday.owner.lname} - {status}",
            'start': holiday.start_date.isoformat(),
            'end': holiday.end_date.isoformat(),
            'allDay': True,
            'color': color,
        })

    # Retrieve all tasks associated with the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 3

    # Query tasks for the current user with pagination
    task_query = Task.query.filter_by(user_id=current_user.id)
    total_tasks = task_query.count()
    total_pages = ceil(total_tasks / per_page)

    # Retrieve the tasks for the current page
    tasks = (
        task_query
        .order_by(Task.due_date)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    # Prepare task events for calendar display
    task_events = [
        {
            'title': task.title,
            'start': task.start_date.isoformat() if task.start_date else
            datetime.now().isoformat(),
            'end': task.due_date.isoformat() if task.due_date else
            datetime.now().isoformat(),
            'type': 'task',
            'description': task.description,
        }
        for task in tasks
    ]

    # Render the dashboard template and pass tasks, holidays, and events
    return render_template("dashboard.html",
                           tasks=tasks, holidays=holidays,
                           holiday_events=holiday_events,
                           task_events=task_events, page=page,
                           total_pages=total_pages)


# Task form route (GET): Displays the form
# to create a new task (accessible only when logged in)
@views.route("/create_task", methods=["GET"])
@login_required
def task_form():
    # Render the create task form template
    return render_template("create_task.html")


# Task creation route (POST): Processes the form
# submission to create a new task (requires login)
@views.route("/create_task", methods=["POST", "GET"])
@login_required
def create_task():
    if request.method == "POST":
        # Retrieve form data submitted by the user
        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority")
        start_date_str = request.form.get("start_date")
        due_date_str = request.form.get("due_date")
        status = request.form.get("status")

        # Convert date strings into datetime objects
        try:
            start_date = datetime.fromisoformat(start_date_str)
            due_date = datetime.fromisoformat(due_date_str)
        except ValueError:
            flash("Invalid date format.", "danger")
            return render_template("create_task.html",
                                   title=title,
                                   description=description,
                                   priority=priority,
                                   start_date=start_date_str,
                                   due_date=due_date_str,
                                   status=status)

        # Validate that due date is not before start date
        if due_date < start_date:
            flash("Due date cannot be before the start date.", "danger")
            return render_template("create_task.html",
                                   title=title,
                                   description=description,
                                   priority=priority,
                                   start_date=start_date_str,
                                   due_date=due_date_str,
                                   status=status)

        # Check if the title length is within limit
        if len(title) > 199:
            flash("Title is too long. Maximum of 200 characters.", "danger")
            return render_template("create_task.html",
                                   title=title,
                                   description=description,
                                   priority=priority,
                                   start_date=start_date_str,
                                   due_date=due_date_str,
                                   status=status)

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

    # If request is GET, render empty create_task form
    return render_template("create_task.html")


# Task editing route 
# (GET/POST): Allows users to edit an existing task (requires login)
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

        # Convert strings into datetime objects
        try:
            start_date = datetime.fromisoformat(start_date_str)
            due_date = datetime.fromisoformat(due_date_str)
        except ValueError:
            flash("Invalid date format.", "danger")
            return render_template("edit_task.html", task=task)

        # Validate due date is not before start date
        if due_date < start_date:
            flash("Due date cannot be before the start date.", "danger")
            return render_template("edit_task.html", task=task)

        # Check if the title length is within limit
        if len(title) > 199:
            flash("Title is too long. Maximum of 200 characters.", "danger")
            return render_template("edit_task.html", task=task)

        # Update task attributes
        task.title = title
        task.description = description
        task.priority = priority
        task.start_date = start_date
        task.due_date = due_date
        task.status = status

        # Commit the changes to the database
        db.session.commit()

        flash("Your task has been successfully updated!", "success")
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
    flash("Task completed and removed.", "success")

    # Redirect back to the dashboard after deletion
    return redirect(url_for("views.dashboard"))


# Route to request a holiday (GET/POST): Allows users to create holiday requests
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
                is_approved=False,  # Initial state is unapproved
                user_id=current_user.id
            )

            # Add the new holiday to the database and commit
            db.session.add(new_holiday)
            db.session.commit()

            flash("Holiday request submitted! Please await approval\
            from admin.", "success")
            return redirect(url_for("views.dashboard"))

        except ValueError:
            flash("Invalid date format. Please use the correct format.", "danger")
            return redirect(url_for("views.request_holiday"))

    # Render the holiday request form if method is GET
    return render_template("request_holiday.html")


# Route to edit a holiday 
# (GET/POST): Allows users or admins to modify holiday requests
@views.route("/edit_holiday/<int:holiday_id>", methods=["GET", "POST"])
@login_required
def edit_holiday(holiday_id):
    # Retrieve the holiday request by its ID
    holiday = Holiday.query.get_or_404(holiday_id)

    # Check authorization: Admins or the request's owner can edit
    if not current_user.is_admin and holiday.user_id != current_user.id:
        flash("You are not authorized to edit this holiday request", "danger")
        return redirect(url_for("views.dashboard"))

    if request.method == "POST":
        # Get updated start and end dates from form
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # Validate presence of both dates
        if not start_date or not end_date:
            flash("Start date and end date are required.", "danger")
            return render_template("edit_holiday.html", holiday=holiday)

        # Validate that start date is before end date
        if start_date >= end_date:
            flash("Start date must be before end date.", "danger")
            return render_template("edit_holiday.html", holiday=holiday)

        # Update holiday request with new dates
        holiday.start_date = start_date
        holiday.end_date = end_date

        # Reset approval status to pending after editing
        holiday.is_approved = False
        holiday.is_declined = False

        # Notify user and commit changes
        flash("Request Updated and sent for approval!", "success")
        db.session.commit()
        return redirect(url_for("views.dashboard"))

    # Render edit form if method is GET
    return render_template("edit_holiday.html", holiday=holiday)


# Route to delete a holiday request
# (POST): Allows users or admins to delete holiday requests
@views.route("/delete_holiday/<int:holiday_id>", methods=["POST"])
@login_required
def delete_holiday(holiday_id):
    # Retrieve the holiday request by its ID
    holiday = Holiday.query.get_or_404(holiday_id)

    # Check authorization for deletion
    if not current_user.is_admin and holiday.user_id != current_user.id:
        flash("You are not authorized to delete this holiday request.", "danger")
        return redirect(url_for("views.dashboard"))

    # Delete the holiday request from the database
    db.session.delete(holiday)
    db.session.commit()
    flash("Holiday request deleted successfully!", "success")

    # Redirect back to dashboard after deletion
    return redirect(url_for("views.dashboard"))


# Route for admin to approve or decline holiday requests (GET/POST)
@views.route("/approve_holiday", methods=["GET", "POST"])
@login_required
def approve_holiday():
    if request.method == "POST":
        # Fetch all unapproved holidays
        unapproved_holidays = (
            Holiday.query.filter_by(is_approved=False, is_declined=False).all()
        )
        for holiday in unapproved_holidays:
            # Check the action (approve/decline) from the form
            holiday_action = request.form.get(f'holiday_action_{holiday.id}')
            if holiday_action == 'approve':
                holiday.is_approved = True
                holiday.is_declined = False
            elif holiday_action == 'decline':
                holiday.is_approved = False
                holiday.is_declined = True

            # Commit the changes for each holiday
            db.session.commit()

        flash("Holiday requests updated successfully.", "success")
        return redirect(url_for("views.dashboard"))

    # If GET, display unapproved holidays for admin review
    unapproved_holidays = (
        Holiday.query.filter_by(is_approved=False, is_declined=False).all()
    )
    return render_template(
        "approve_holiday.html", holidays=unapproved_holidays
    )
