import sqlite3

def verify_categories():
    print("Checking categories in recipes.db...")
    
    try:
        # Connect to recipes.db
        conn = sqlite3.connect('instance/recipes.db')
        cursor = conn.cursor()
        
        # Check categories table
        print("\nRecipe Categories:")
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        print(f"Found {len(categories)} recipe categories:")
        for cat in categories:
            print(f"- {cat[1]}")  # cat[1] is the name column
            
        # Check ingredient_categories table
        print("\nIngredient Categories:")
        cursor.execute("SELECT * FROM ingredient_categories ORDER BY name")
        ingredients = cursor.fetchall()
        print(f"Found {len(ingredients)} ingredient categories:")
        for ing in ingredients:
            print(f"- {ing[1]}")  # ing[1] is the name column
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_categories() 