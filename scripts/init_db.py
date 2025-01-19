import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions import db
from models.models import Category, User
from werkzeug.security import generate_password_hash
from main import app  # Import the app directly instead of create_app

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()

        # Add default categories if they don't exist
        categories = [
            'Breakfast', 'Lunch', 'Dinner', 'Dessert', 
            'Snacks', 'Beverages', 'Appetizers', 'Soups'
        ]
        
        for cat_name in categories:
            if not Category.query.filter_by(name=cat_name).first():
                category = Category(name=cat_name)
                db.session.add(category)

        # Add admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)

        try:
            db.session.commit()
            print("Database initialized successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {e}")

if __name__ == '__main__':
    init_db() 