import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

if os.path.exists("env.py"):
    import env  # noqa

db = SQLAlchemy()
DB_NAME = "nightsapp.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/views')
    app.register_blueprint(auth, url_prefix='/')

    return app


def create_database(app):
    if not path.exists('nightsapp/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')