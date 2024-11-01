import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .database import db
from .models import User
from flask_login import LoginManager
if os.path.exists("env.py"):
    import env  # noqa


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db.init_app(app)
  
from .views import views
from .auth import auth


with app.app_context():
    db.create_all()

app.register_blueprint(views, url_prefix='/views')
app.register_blueprint(auth, url_prefix='/')

login_manager = LoginManager()
login_manager.login_view = 'views.dashboard'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"]) #debugging

    





