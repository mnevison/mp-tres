from .database import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Enum

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(150), nullable=False)
    lname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(300), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default= True)
    holidays = db.relationship('Holiday', backref='owner', lazy=True)

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

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="pending")
    priority = db.Column(db.Enum('low', 'medium', 'high', name='priority_levels'), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=True) 
    due_date = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
    
    def __repr__(self):
        return f'<Task {self.title} by User {self.user_id}>'

class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"<UserHoliday {self.user_id} from {self.start_date} to {self.end_date}>"
