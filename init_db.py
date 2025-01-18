import json
import os
import sqlite3


def init_db():
    # Create instance directory if it doesn't exist
    if not os.path.exists('instance'):
        os.makedirs('instance')

    # Database path
    DB_PATH = 'instance/recipes.db'

    # Remove old database if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Removed old database")

    # Create new database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Create tables with updated users table
        cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            email TEXT,
            avatar TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
        ''')

        # Create recipes_images table with image field
        cursor.execute('''
        CREATE TABLE recipes_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            prep_time INTEGER,
            servings INTEGER,
            instructions TEXT,
            image TEXT
        )
        ''')

        # Create ingredients table
        cursor.execute('''
        CREATE TABLE ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            amount REAL,
            unit TEXT,
            description TEXT,
            category TEXT
        )
        ''')

        # Add admin user
        cursor.execute('''
        INSERT INTO users (username, password, role) 
        VALUES ('admin', 'admin123', 'admin')
        ''')

        # Load and process recipes_images from JSON
        with open('recipes.json', 'r', encoding='utf-8') as file:
            recipes = json.load(file)

        total_ingredients = 0

        for recipe in recipes:
            # Insert recipe
            cursor.execute('''
                INSERT INTO recipes_images (
                    user_id,
                    name,
                    category,
                    description,
                    prep_time,
                    servings,
                    instructions,
                    image
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                1,  # Default user_id
                recipe['name'],
                recipe.get('category', 'Other'),
                recipe.get('description', ''),
                0,  # Default prep_time
                4,  # Default servings
                '\n'.join(recipe.get('instructions', [])) if 'instructions' in recipe else '',
                recipe.get('image_path', '')
            ))

            recipe_id = cursor.lastrowid

            # Insert ingredients
            for ingredient in recipe.get('ingredients', []):
                # Handle both name formats in your JSON
                ingredient_name = ingredient.get('ingredient', ingredient.get('name', ''))
                if ingredient_name:  # Only insert if we have a name
                    cursor.execute('''
                        INSERT INTO ingredients (
                            recipe_id,
                            name,
                            amount,
                            unit,
                            description,
                            category
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        recipe_id,
                        ingredient_name,
                        ingredient.get('quantity', 0),
                        ingredient.get('unit', ''),
                        ingredient.get('description', ''),
                        ingredient.get('category', 'Other')
                    ))
                    total_ingredients += 1

        # Commit all changes
        conn.commit()

        # Verify data
        cursor.execute("SELECT COUNT(*) FROM recipes_images")
        recipe_count = cursor.fetchone()[0]

        print(f"\nDatabase created with:")
        print(f"- {recipe_count} recipes_images")
        print(f"- {total_ingredients} ingredients")

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        raise

    finally:
        conn.close()
        print(f"Database created at: {os.path.abspath(DB_PATH)}")


if __name__ == '__main__':
    init_db()
