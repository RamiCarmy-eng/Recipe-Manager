from flask import Flask
from extensions import db
from models.models import *
import os

def create_app():
    app = Flask(__name__)
    # Use the database file in the current directory
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def check_current_db():
    if not os.path.exists('recipes.db'):
        print("\nError: recipes.db not found in current directory!")
        return

    print(f"\n=== Checking recipes.db ===")
    print(f"Database size: {os.path.getsize('recipes.db'):,} bytes")
    
    tables = {
        'Users': User,
        'Recipes': Recipe,
        'Categories': Category,
        'Ingredients': Ingredient,
        'Comments': Comment,
        'Favorites': Favorite,
        'UserPreferences': UserPreference,
        'ShoppingLists': ShoppingList,
        'CollaborativeLists': CollaborativeList,
        'UserActivities': UserActivity
    }

    empty_tables = []
    for name, model in tables.items():
        try:
            count = db.session.query(model).count()
            print(f"{name}: {count} rows")
            if count == 0:
                empty_tables.append(name)
        except Exception as e:
            print(f"Error with {name}: {str(e)}")
    
    return empty_tables

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        empty_tables = check_current_db()
        if empty_tables:
            print("\nEmpty tables that need population:")
            for table in empty_tables:
                print(f"- {table}") 