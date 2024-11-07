from flask import Blueprint, render_template, redirect, url_for

# Define a blueprint for error handling
errors = Blueprint('errors', __name__)

@errors.route("/error/<int:error_code>")
def error_handler(error_code):
    # Custom error messages for specific HTTP error codes
    error_messages = {
        404: "Something went wrong! The page didn't load correctly or is unavailable.",
        500: "Internal server error. Please try again later.",
        401: "Unauthorized access. You need to log in to view this page."
    }
    # Fetch the error message or use a default message
    error_message = error_messages.get(
        error_code, "An unexpected error occurred."
    )
    # Render the error template with the appropriate error message
    return render_template(
        "error_handler.html",
        error_number=error_code,
        error_message=error_message
    ), error_code

# Handle 404 errors globally and redirect to the custom error handler
@errors.app_errorhandler(404)
def handle_404(e):
    return redirect(url_for("errors.error_handler", error_code=404))

# Handle 500 errors globally and redirect to the custom error handler
@errors.app_errorhandler(500)
def handle_500(e):
    return redirect(url_for("errors.error_handler", error_code=500))

# Handle 401 errors globally and redirect to the custom error handler
@errors.app_errorhandler(401)
def handle_401(e):
    return redirect(url_for("errors.error_handler", error_code=401))
