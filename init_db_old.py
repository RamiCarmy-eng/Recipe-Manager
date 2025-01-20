import json
import os
import sqlite3
import time
from wsgiO import app, db
from models.models import User, Recipe, Ingredient
from werkzeug.security import generate_password_hash


def init_db():
    # Create instance directory if it doesn't exist
    if not os.path.exists('instance'):
        os.makedirs('instance')

    # Database path
    DB_PATH = 'instance/recipes.db'

    # Try to remove the old database
    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        try:
            if os.path.exists(DB_PATH):
                os.remove(DB_PATH)
                print("Removed old database")
                break
        except PermissionError:
            attempt += 1
            print(f"Database is locked. Attempt {attempt} of {max_attempts}...")
            time.sleep(1)  # Wait for 1 second before trying again

            # On the last attempt, try to close all connections
            if attempt == max_attempts - 1:
                try:
                    with app.app_context():
                        db.session.remove()
                        db.engine.dispose()
                except:
                    pass

    if attempt == max_attempts:
        print("Could not remove the old database. Please close any applications using it and try again.")
        return

    with app.app_context():
        # Create all tables using SQLAlchemy
        db.create_all()

        try:
            # Add admin user
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()

            # Load and process recipes from JSON
            with open('recipes.json', 'r', encoding='utf-8') as file:
                recipes_data = json.load(file)

            total_ingredients = 0

            for recipe_data in recipes_data:
                # Create recipe
                recipe = Recipe(
                    user_id=admin_user.id,
                    name=recipe_data['name'],
                    category=recipe_data.get('category', 'Other'),
                    subcategory=recipe_data.get('subcategory', ''),
                    description=recipe_data.get('description', ''),
                    prep_time=0,
                    servings=4,
                    instructions='\n'.join(
                        recipe_data.get('instructions', [])) if 'instructions' in recipe_data else '',
                    image=recipe_data.get('image_path', '')
                )
                db.session.add(recipe)
                db.session.flush()

                # Add ingredients
                for ing_data in recipe_data.get('ingredients', []):
                    ingredient_name = ing_data.get('ingredient', ing_data.get('name', ''))
                    if ingredient_name:
                        ingredient = Ingredient(
                            recipe_id=recipe.id,
                            name=ingredient_name,
                            amount=ing_data.get('quantity', 0),
                            unit=ing_data.get('unit', ''),
                            description=ing_data.get('description', ''),
                            category=ing_data.get('category', 'Other')
                        )
                        db.session.add(ingredient)
                        total_ingredients += 1

            # Commit all changes
            db.session.commit()

            # Verify data
            recipe_count = Recipe.query.count()
            ingredient_count = Ingredient.query.count()

            print(f"\nDatabase created with:")
            print(f"- {recipe_count} recipes")
            print(f"- {ingredient_count} ingredients")

        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            raise
        finally:
            db.session.close()
            db.engine.dispose()

        print(f"Database created at: {os.path.abspath(DB_PATH)}")


if __name__ == '__main__':
    try:
        # Try to close any existing connections
        with app.app_context():
            db.session.remove()
            db.engine.dispose()
    except:
        pass

    init_db()
