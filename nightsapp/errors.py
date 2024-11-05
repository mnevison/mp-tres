from flask import Blueprint, render_template, redirect, url_for

errors = Blueprint('errors', __name__)

@errors.route("/error/<int:error_code>")
def error_handler(error_code):
    error_messages = {
        404: "Something went wrong! The page didn't load correctly or is unavailable.",
        500: "Internal server error. Please try again later.",
        401: "Unauthorized access. You need to log in to view this page."
    }
    error_message = error_messages.get(error_code, "An unexpected error occurred.")
    return render_template(
        "error_handler.html",
        error_number=error_code,
        error_message=error_message
    ), error_code

@errors.app_errorhandler(404)
def handle_404(e):
    return redirect(url_for("errors.error_handler", error_code=404))

@errors.app_errorhandler(500)
def handle_500(e):
    return redirect(url_for("errors.error_handler", error_code=500))

@errors.app_errorhandler(401)
def handle_401(e):
    return redirect(url_for("errors.error_handler", error_code=401))

