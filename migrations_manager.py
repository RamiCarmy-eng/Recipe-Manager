from wsgiO import app, db
from flask_migrate import Migrate, upgrade

migrate = Migrate(app, db)

def init_db():
    with app.app_context():
        # Import all models here
        from models.models import Recipe, User  # Import all your models
        
        # Create tables
        db.create_all()
        
        # Add new column if it doesn't exist
        with db.engine.connect() as conn:
            try:
                conn.execute('ALTER TABLE recipes ADD COLUMN IF NOT EXISTS subcategory VARCHAR(100)')
                db.session.commit()
                print("Database initialized successfully")
            except Exception as e:
                print(f"Error initializing database: {e}")
                db.session.rollback()

if __name__ == '__main__':
    init_db() 