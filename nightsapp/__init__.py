import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
if os.path.exists("env.py"):
    import env  # noqa



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
db = SQLAlchemy(app)
migrate = Migrate()

migrate.init_app(app, db)
    

from .views import views
from .auth import auth
from .models import User

app.register_blueprint(views, url_prefix='/views')
app.register_blueprint(auth, url_prefix='/')

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    





