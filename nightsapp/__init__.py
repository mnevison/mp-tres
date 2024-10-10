import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .database import db
from .models import User
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")

db.init_app(app)
   
from .views import views
from .auth import auth


with app.app_context():
    db.create_all()

app.register_blueprint(views, url_prefix='/views')
app.register_blueprint(auth, url_prefix='/')

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')


    





