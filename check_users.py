from wsgi import app
from models import User
from extensions import db

with app.app_context():
    users = User.query.all()
    print("\nAll users in database:")
    for user in users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Password hash: {user.password}")
        print("-" * 50)