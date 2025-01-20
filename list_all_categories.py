from app import create_app
from models.models import Category, IngredientCategory
import sqlite3

def list_categories_from_db():
    print("Checking categories directly from database...")
    try:
        # Connect directly to the database
        conn = sqlite3.connect('instance/recipes.db')
        cursor = conn.cursor()
        
        # Check categories table
        print("\nRecipe Categories:")
        cursor.execute("SELECT name FROM categories ORDER BY name")
        categories = cursor.fetchall()
        for cat in categories:
            print(f"- {cat[0]}")
            
        # Check ingredient_categories table
        print("\nIngredient Categories:")
        cursor.execute("SELECT name FROM ingredient_categories ORDER BY name")
        ingredients = cursor.fetchall()
        for ing in ingredients:
            print(f"- {ing[0]}")
            
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_categories_from_db() 