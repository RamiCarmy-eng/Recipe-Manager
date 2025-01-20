from wsgi import app, db
from models.models import *


def recreate_database():
    with app.app_context():
        # Backup existing data if needed
        try:
            # Get existing data
            users = User.query.all()
            # Add more tables as needed

            # Drop and recreate all tables
            db.drop_all()
            db.create_all()

            # Restore data if needed
            for user in users:
                db.session.add(user)

            db.session.commit()
            print("Database recreated successfully!")

        except Exception as e:
            print(f"Error recreating database: {e}")
            db.session.rollback()


if __name__ == "__main__":
    recreate_database()