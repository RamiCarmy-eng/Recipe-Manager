import sqlite3


def test_database():
    db = sqlite3.connect('instance/recipes.db')
    cursor = db.cursor()

    try:
        # Test 1: Count recipes
        cursor.execute('SELECT COUNT(*) FROM recipes')
        recipe_count = cursor.fetchone()[0]
        print(f"Total recipes in database: {recipe_count}")

        # Test 2: Count ingredients
        cursor.execute('SELECT COUNT(*) FROM ingredients')
        ingredient_count = cursor.fetchone()[0]
        print(f"Total ingredients in database: {ingredient_count}")

        # Test 3: Check a specific recipe with its ingredients
        cursor.execute('''
            SELECT r.name, r.category, r.image, COUNT(i.id) as ingredient_count
            FROM recipes r
            LEFT JOIN ingredients i ON r.id = i.recipe_id
            GROUP BY r.id
            LIMIT 3
        ''')
        recipes = cursor.fetchall()

        print("\nSample of 3 recipes with their ingredient counts:")
        for recipe in recipes:
            print(f"\nRecipe: {recipe[0]}")
            print(f"Category: {recipe[1]}")
            print(f"Image path: {recipe[2]}")
            print(f"Number of ingredients: {recipe[3]}")

            # Get ingredients for this recipe
            cursor.execute('''
                SELECT name, amount, unit, category
                FROM ingredients
                WHERE recipe_id = (
                    SELECT id FROM recipes WHERE name = ?
                )
            ''', (recipe[0],))

            ingredients = cursor.fetchall()
            print("\nIngredients:")
            for ing in ingredients:
                print(f"- {ing[0]}: {ing[1]} {ing[2]} ({ing[3]})")

    except Exception as e:
        print(f"Error during testing: {str(e)}")

    finally:
        db.close()


if __name__ == '__main__':
    test_database()
