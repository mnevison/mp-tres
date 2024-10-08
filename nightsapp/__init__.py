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
    

    from .routes import main as main_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app


def create_database(app):
    if not path.exists('nightsapp/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')