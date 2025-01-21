import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from extensions import db
from models.models import *
from sqlalchemy import text

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def add_ingredient_id_column():
    try:
        with db.engine.connect() as conn:
            # Using text() for the SQL command
            sql = text('ALTER TABLE shopping_list_items ADD COLUMN ingredient_id INTEGER REFERENCES ingredients(id)')
            conn.execute(sql)
            conn.commit()
            print("Successfully added ingredient_id column to shopping_list_items table")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Detailed error information:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        
        # Print current table structure
        try:
            with db.engine.connect() as conn:
                result = conn.execute(text("PRAGMA table_info(shopping_list_items)"))
                print("\nCurrent table structure:")
                for row in result:
                    print(row)
        except Exception as table_e:
            print(f"Could not get table structure: {str(table_e)}")
        raise e

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        add_ingredient_id_column() 