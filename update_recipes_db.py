import json
import sqlite3


def cleanup_database():
    db = sqlite3.connect('instance/recipes.db')
    cursor = db.cursor()

    try:
        cursor.execute('BEGIN TRANSACTION')

        # Delete all records from both tables
        cursor.execute('DELETE FROM ingredients')
        cursor.execute('DELETE FROM recipes_images')

        # Reset the auto-increment counters
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="recipes_images"')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="ingredients"')

        cursor.execute('COMMIT')
        print("Successfully cleaned up the database!")

    except Exception as e:
        cursor.execute('ROLLBACK')
        print(f"Error during cleanup: {str(e)}")

    finally:
        db.close()


def get_recipe_category(recipe):
    name = recipe['name'].lower()

    # Define category mappings
    categories = {
        'dessert': ['cake', 'cookies', 'pie', 'chocolate'],
        'breakfast': ['pancakes', 'breakfast'],
        'soup': ['soup', 'broth'],
        'salad': ['salad'],
        'main dish': ['aloo', 'couscous', 'spaghetti', 'chicken'],
        'appetizer': ['pickled', 'appetizer'],
        'seafood': ['fish', 'seafood']
    }

    # Check recipe name against categories
    for category, keywords in categories.items():
        if any(keyword in name for keyword in keywords):
            return category.title()

    # Check ingredients for category hints
    ingredients = [ing.get('ingredient', '').lower() for ing in recipe['ingredients']]
    if any('fish' in ing for ing in ingredients):
        return 'Seafood'
    elif any('chicken' in ing for ing in ingredients):
        return 'Main Dish'

    return 'Main Dish'  # Default category


def populate_database():
    db = sqlite3.connect('instance/recipes.db')
    cursor = db.cursor()

    with open('recipes.json', 'r', encoding='utf-8') as file:
        recipes = json.load(file)

    try:
        cursor.execute('BEGIN TRANSACTION')

        for recipe in recipes:
            # Insert recipe with proper category
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
                get_recipe_category(recipe),
                recipe.get('description', ''),
                30,  # Default prep_time
                4,  # Default servings
                '\n'.join(recipe.get('instructions', [])) if 'instructions' in recipe else '',
                recipe.get('image_path', '')
            ))

            recipe_id = cursor.lastrowid

            # Insert ingredients
            for ingredient in recipe['ingredients']:
                # Convert quantity to float if possible
                try:
                    quantity = float(ingredient.get('quantity', 0)) if ingredient.get('quantity') is not None else 0
                except (ValueError, TypeError):
                    quantity = 0

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
                    ingredient.get('ingredient', ingredient.get('name', '')),
                    quantity,
                    ingredient.get('unit', ''),
                    ingredient.get('description', ''),
                    ingredient.get('category', 'Other')
                ))

        cursor.execute('COMMIT')
        print("Successfully populated database with recipes_images and ingredients!")

    except Exception as e:
        cursor.execute('ROLLBACK')
        print(f"Error: {str(e)}")
        raise

    finally:
        db.close()


def verify_database():
    db = sqlite3.connect('instance/recipes.db')
    cursor = db.cursor()

    try:
        # Count recipes_images
        cursor.execute('SELECT COUNT(*) FROM recipes_images')
        recipe_count = cursor.fetchone()[0]
        print(f"\nTotal recipes_images in database: {recipe_count}")

        # Count ingredients
        cursor.execute('SELECT COUNT(*) FROM ingredients')
        ingredient_count = cursor.fetchone()[0]
        print(f"Total ingredients in database: {ingredient_count}")

        # Sample of recipes_images
        cursor.execute('''
            SELECT r.name, r.category, r.image, COUNT(i.id) as ingredient_count
            FROM recipes_images r
            LEFT JOIN ingredients i ON r.id = i.recipe_id
            GROUP BY r.id
            LIMIT 3
        ''')
        recipes = cursor.fetchall()

        print("\nSample of 3 recipes_images with their ingredient counts:")
        for recipe in recipes:
            print(f"\nRecipe: {recipe[0]}")
            print(f"Category: {recipe[1]}")
            print(f"Image path: {recipe[2]}")
            print(f"Number of ingredients: {recipe[3]}")

            cursor.execute('''
                SELECT name, amount, unit, category
                FROM ingredients
                WHERE recipe_id = (
                    SELECT id FROM recipes_images WHERE name = ?
                )
            ''', (recipe[0],))

            ingredients = cursor.fetchall()
            print("\nIngredients:")
            for ing in ingredients:
                print(f"- {ing[0]}: {ing[1]} {ing[2]} ({ing[3]})")

    except Exception as e:
        print(f"Error during verification: {str(e)}")

    finally:
        db.close()


if __name__ == '__main__':
    print("Starting database update process...")
    cleanup_database()
    populate_database()
    verify_database()
    print("\nDatabase update completed!")
