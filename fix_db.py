import os
from wsgiO import app, db
from models.models import User, Recipe, Ingredient, Comment, Category, Favorite
from models.models import ShoppingList, ShoppingListItem, CollaborativeList, UserActivity
from flask import Flask
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def check_and_fix_database():
    # First ensure instance directory exists
    instance_dir = 'instance'
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"Created instance directory at: {os.path.abspath(instance_dir)}")

    with app.app_context():
        try:
            print("\nChecking database integrity...")
            
            # Ensure all tables exist
            db.create_all()
            
            # Check if tables exist and have data
            users = User.query.all()
            recipes = Recipe.query.all()
            ingredients = Ingredient.query.all()
            comments = Comment.query.all()
            categories = Category.query.all()
            favorites = Favorite.query.all()
            shopping_lists = ShoppingList.query.all()
            activities = UserActivity.query.all()
            
            print(f"\nCurrent database status:")
            print(f"- Users: {len(users)}")
            print(f"- Recipes: {len(recipes)}")
            print(f"- Ingredients: {len(ingredients)}")
            print(f"- Comments: {len(comments)}")
            print(f"- Categories: {len(categories)}")
            print(f"- Favorites: {len(favorites)}")
            print(f"- Shopping Lists: {len(shopping_lists)}")
            print(f"- User Activities: {len(activities)}")
            
            # Check recipe-ingredient relationships
            print("\nChecking recipe-ingredient relationships...")
            orphaned_ingredients = []
            for ingredient in ingredients:
                if not Recipe.query.get(ingredient.recipe_id):
                    print(f"Found orphaned ingredient: {ingredient.name}")
                    orphaned_ingredients.append(ingredient)
            
            # Check recipes without ingredients
            empty_recipes = []
            for recipe in recipes:
                if not recipe.ingredients:
                    print(f"Found recipe without ingredients: {recipe.name}")
                    empty_recipes.append(recipe)
            
            # Check user-recipe relationships
            orphaned_recipes = []
            for recipe in recipes:
                if not User.query.get(recipe.user_id):
                    print(f"Found recipe without user: {recipe.name}")
                    orphaned_recipes.append(recipe)
            
            print("\nDatabase check complete!")
            
            if not (orphaned_ingredients or empty_recipes or orphaned_recipes):
                print("No issues found - database is healthy!")
                return True
                
            print("\nIssues found:")
            if orphaned_ingredients:
                print(f"- {len(orphaned_ingredients)} orphaned ingredients")
            if empty_recipes:
                print(f"- {len(empty_recipes)} recipes without ingredients")
            if orphaned_recipes:
                print(f"- {len(orphaned_recipes)} recipes without users")
                
            # Ask before making any changes
            if input("\nWould you like to fix these issues? (y/n): ").lower() == 'y':
                # Fix orphaned ingredients
                for ingredient in orphaned_ingredients:
                    print(f"Removing orphaned ingredient: {ingredient.name}")
                    db.session.delete(ingredient)
                
                # Mark empty recipes
                for recipe in empty_recipes:
                    print(f"Recipe without ingredients: {recipe.name}")
                
                # Fix orphaned recipes
                for recipe in orphaned_recipes:
                    print(f"Removing recipe without user: {recipe.name}")
                    db.session.delete(recipe)
                
                db.session.commit()
                print("\nFixed database issues!")
            else:
                print("\nNo changes made to database.")
            
            return True
            
        except Exception as e:
            print(f"Error checking database: {str(e)}")
            db.session.rollback()
            return False

def fix_database():
    with app.app_context():
        db.session.execute('ALTER TABLE shopping_list_items DROP COLUMN ingredient_id')
        db.session.execute('ALTER TABLE recipe_ingredients DROP COLUMN ingredient_id')
        db.session.commit()
        print("Database structure fixed!")

app = create_app()

if __name__ == '__main__':
    # Ensure the database file exists
    db_path = os.path.join('instance', 'recipes.db')
    if not os.path.exists(db_path):
        print(f"Database file not found at: {os.path.abspath(db_path)}")
        print("Running database initialization...")
        with app.app_context():
            db.create_all()
            print("Database initialized.")
    
    check_and_fix_database()
    fix_database() 