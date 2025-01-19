import sqlite3
from wsgi import app, db
from models.models import User, Recipe, Ingredient

"""def check_db():
    conn = sqlite3.connect('instance/recipes_images.db')
    c = conn.cursor()

    print("\nChecking database contents:")

    # Check users
    c.execute("SELECT COUNT(*) FROM users")
    print(f"Users count: {c.fetchone()[0]}")

    # Check recipes_images
    c.execute("SELECT COUNT(*) FROM recipes_images")
    print(f"Recipes count: {c.fetchone()[0]}")

    # Check ingredients
    c.execute("SELECT COUNT(*) FROM ingredients")
    print(f"Ingredients count: {c.fetchone()[0]}")

    conn.close()"""


def test_database():
    db = sqlite3.connect('Recipe-Master/instance/recipes_images.db')
    cursor = db.cursor()

    try:
        # Test 1: Count recipes_images
        cursor.execute('SELECT COUNT(*) FROM recipes_images')
        recipe_count = cursor.fetchone()[0]
        print(f"Total recipes_images in database: {recipe_count}")

        # Test 2: Count ingredients
        cursor.execute('SELECT COUNT(*) FROM ingredients')
        ingredient_count = cursor.fetchone()[0]
        print(f"Total ingredients in database: {ingredient_count}")

        # Test 3: Check a specific recipe with its ingredients
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

            # Get ingredients for this recipe
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
        print(f"Error during testing: {str(e)}")

    finally:
        db.close()


def check_database():
    with app.app_context():
        try:
            # Check users
            users = User.query.all()
            print("\nUsers in database:")
            for user in users:
                print(f"- {user.username} (role: {user.role})")

            # Check recipes
            recipes = Recipe.query.all()
            print("\nRecipes in database:")
            for recipe in recipes:
                print(f"\nRecipe: {recipe.name}")
                print(f"Category: {recipe.category}")
                print(f"Subcategory: {recipe.subcategory}")
                print("Ingredients:")
                for ingredient in recipe.ingredients:
                    print(f"- {ingredient.name}: {ingredient.amount} {ingredient.unit}")

            print(f"\nTotal counts:")
            print(f"- Users: {len(users)}")
            print(f"- Recipes: {len(recipes)}")
            print(f"- Ingredients: {sum(len(recipe.ingredients) for recipe in recipes)}")

        except Exception as e:
            print(f"Error checking database: {str(e)}")


if __name__ == '__main__':
    # check_db()

    test_database()
    check_database()
