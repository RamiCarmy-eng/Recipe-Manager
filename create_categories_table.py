from app import create_app
from extensions import db
from models.models import Category
from sqlalchemy import text

def create_categories_table():
    app = create_app()
    with app.app_context():
        # Create only the categories table
        print("Creating categories table...")
        
        # Get SQL for creating the table
        sql = text("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE
        );
        """)
        
        try:
            db.session.execute(sql)
            db.session.commit()
            print("Categories table created successfully!")
        except Exception as e:
            print(f"Error creating table: {e}")

if __name__ == "__main__":
    create_categories_table() 