from wsgi import app
from models import User
from extensions import db

with app.app_context():
    # Get the admin user
    user = User.query.filter_by(username='admin').first()
    if user:
        # Set a new password
        user.set_password('admin123')
        db.session.commit()
        print("Password reset to: admin123")
    else:
        print("Admin user not found!")