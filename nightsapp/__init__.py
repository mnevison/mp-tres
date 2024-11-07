import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .database import db
from .models import User
from flask_login import LoginManager
from .views import views
from .auth import auth
from .errors import errors

# Load environment variables if present
if os.path.exists("env.py"):
    import env  # noqa

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Configure database URI based on environment
if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

# Initialize the database
db.init_app(app)

# Create all tables within the application context
with app.app_context():
    db.create_all()

# Register blueprints for modular structure
app.register_blueprint(views, url_prefix='/views')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(errors)

# Setup Flask-Login for session management
login_manager = LoginManager()
login_manager.login_view = 'views.dashboard'
login_manager.init_app(app)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
