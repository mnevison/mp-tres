from nightsapp import app, db  # Import your db object from your application
db.drop_all()  # Drop all tables
db.create_all()