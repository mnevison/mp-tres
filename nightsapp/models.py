from .database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(150), nullable=False)
    lname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(300), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default= True)

    @property
    def is_authenticated(self):
        return True  # All users logged in are authenticated

    @property
    def is_anonymous(self):
        return False  # Regular users are not anonymous

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.fname} {self.lname}>'