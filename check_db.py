import os
from flask import Flask
from app import create_app
from extensions import db
from models.models import Recipe, Category, Ingredient, User, Comment, Favorite, UserPreference, IngredientCategory, ShoppingList, ShoppingListItem, ShoppingListTemplate, TemplateItem, CollaborativeList, CollaborativeListMember, CollaborativeListItem, RecipeIngredient, UserActivity

app = create_app()

def check_db():
    print("Starting database check...")
    
    # Print current working directory
    print(f"Current directory: {os.getcwd()}")
    
    # Print database URI from config
    print(f"Database URI from config: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Check instance folder
    instance_path = os.path.join(os.getcwd(), 'instance')
    print(f"Instance path: {instance_path}")
    if os.path.exists(instance_path):
        print("Instance folder exists")
        print("Contents:", os.listdir(instance_path))
    else:
        print("Instance folder does not exist")
    
    try:
        with app.app_context():
            # Try to connect and get tables
            tables = db.engine.table_names()
            print("\nFound tables:", tables)
    except Exception as e:
        print(f"\nError connecting to database: {str(e)}")

def check_db_content():
    with app.app_context():
        print("\nChecking Categories:")
        categories = Category.query.all()
        for cat in categories:
            print(f"- {cat.name}")

        print("\nChecking Recipes:")
        recipes = Recipe.query.all()
        for recipe in recipes:
            print(f"- {recipe.name} (Category: {recipe.category})")

        print("\nChecking Ingredients:")
        ingredients = Ingredient.query.all()
        for ing in ingredients:
            print(f"- {ing.name}")

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def check_database():
    print("\n=== Database Table Contents ===")
    tables = {
        'Users': User,
        'Recipes': Recipe,
        'Categories': Category,
        'Ingredients': Ingredient,
        'Comments': Comment,
        'Favorites': Favorite,
        'UserPreferences': UserPreference,
        'IngredientCategories': IngredientCategory,
        'ShoppingLists': ShoppingList,
        'ShoppingListItems': ShoppingListItem,
        'ShoppingListTemplates': ShoppingListTemplate,
        'TemplateItems': TemplateItem,
        'CollaborativeLists': CollaborativeList,
        'CollaborativeListMembers': CollaborativeListMember,
        'CollaborativeListItems': CollaborativeListItem,
        'RecipeIngredients': RecipeIngredient,
        'UserActivities': UserActivity
    }

    for name, model in tables.items():
        try:
            count = db.session.query(model).count()
            print(f"{name}: {count} rows")
        except Exception as e:
            print(f"Error with {name}: {str(e)}")

if __name__ == "__main__":
    check_db()
    check_db_content()
    with app.app_context():
        check_database()
