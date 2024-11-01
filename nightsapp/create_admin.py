from nightsapp import app, db
from nightsapp.models import User

with app.app_context():

    # admin_user = User(fname="Admin", lname="User", email="admin@example.com", password="securepassword", is_admin=True)
    # db.session.add(admin_user)
    # db.session.commit()

    user = User.query.filter_by(email="mnevison2@gmail.com").first()
    if user:
        user.is_admin = True
        db.session.commit()

print("Admin user created or updated.")