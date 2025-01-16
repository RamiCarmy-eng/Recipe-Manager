from werkzeug.security import generate_password_hash
from models import User
from extensions import db

def hash_admin_password():
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if admin:
            # Hash the plain password that's currently in the DB
            admin.password = generate_password_hash('admin123')
            db.session.commit()
            print("Admin password has been hashed")