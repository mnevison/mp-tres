import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .database import db
from .models import User
if os.path.exists("env.py"):
    import env  # noqa


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")

db.init_app(app)
  
from .views import views
from .auth import auth


with app.app_context():
    db.create_all()

app.register_blueprint(views, url_prefix='/views')
app.register_blueprint(auth, url_prefix='/')

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"]) #debugging

    





