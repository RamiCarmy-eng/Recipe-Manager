import json
import sqlite3


def populate_database():
    db = sqlite3.connect('instance/recipes.db')
    cursor = db.cursor()

    with open('recipes.json', 'r', encoding='utf-8') as file:
        recipes = json.load(file)

    try:
        cursor.execute('BEGIN TRANSACTION')

        for recipe in recipes:
            cursor.execute('''
                INSERT INTO recipes (
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
                recipe.get('image_path', '')  # Add image path from JSON
            ))

            recipe_id = cursor.lastrowid

            # Insert ingredients (unchanged)
            for ingredient in recipe['ingredients']:
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
                    ingredient.get('quantity', 0),
                    ingredient.get('unit', ''),
                    ingredient.get('description', ''),
                    ingredient.get('category', 'Other')
                ))

        cursor.execute('COMMIT')
        print("Successfully populated database with recipes and ingredients!")

    except Exception as e:
        cursor.execute('ROLLBACK')
        print(f"Error: {str(e)}")
        raise

    finally:
        db.close()


if __name__ == '__main__':
    # Then populate the database
    populate_database()
