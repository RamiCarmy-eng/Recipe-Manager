from wsgi import app, db
from models.models import Category, IngredientCategory
from sqlalchemy import text

def populate_categories():
    # Main recipe categories with all subcategories
    recipe_categories = [
        # Breakfast & Brunch
        "Breakfast", "Brunch", "Hot Cereals", "Eggs & Omelettes", "Pancakes & Waffles", 
        "Breakfast Sandwiches", "Smoothie Bowls", "Breakfast Burritos", "French Toast",
        "Breakfast Casseroles", "Quiche", "Muffins", "Scones", "Breakfast Pastries",
        
        # Lunch & Dinner
        "Lunch", "Dinner", "Sandwiches & Wraps", "Quick Meals", "Family Dinners", 
        "One-Pot Meals", "Sheet Pan Dinners", "Casseroles", "Stir-Fries",
        
        # Main Dishes by Protein
        "Beef Dishes", "Pork Dishes", "Chicken Dishes", "Turkey Dishes", "Fish Dishes", 
        "Seafood Dishes", "Lamb Dishes", "Game Meat", "Tofu Dishes", "Bean Dishes",
        
        # International Cuisines
        "Italian", "Mexican", "Chinese", "Japanese", "Thai", "Indian", "Korean",
        "Vietnamese", "Mediterranean", "French", "Greek", "Middle Eastern", "Spanish",
        "American", "German", "Brazilian", "Caribbean", "African", "British",
        
        # Course Types
        "Appetizers", "Soups", "Stews", "Salads", "Main Dishes", "Side Dishes",
        "Dips & Spreads", "Finger Foods", "Party Snacks", "Cheese Plates", "Bruschetta",
        
        # Pasta & Grains
        "Pasta Dishes", "Rice Dishes", "Noodle Dishes", "Risotto", "Quinoa Dishes",
        "Couscous", "Grain Bowls", "Mac and Cheese", "Lasagna", "Spaghetti",
        
        # Vegetables & Sides
        "Vegetable Dishes", "Potato Dishes", "Roasted Vegetables", "Grilled Vegetables",
        "Vegetable Stir-Fries", "Salad Bowls", "Vegetable Soups", "Vegetable Curries",
        
        # Baking & Desserts
        "Desserts", "Cakes", "Pies", "Cookies", "Brownies", "Ice Cream", "Puddings",
        "Cheesecakes", "Tarts", "Pastries", "Bread", "Muffins", "Cupcakes", "Donuts",
        
        # Special Diets
        "Vegetarian", "Vegan", "Gluten-Free", "Low-Carb", "Keto", "Paleo",
        "Dairy-Free", "Nut-Free", "Low-Fat", "Low-Sodium", "Sugar-Free",
        
        # Cooking Methods
        "Grilled", "Baked", "Roasted", "Fried", "Steamed", "Slow Cooker",
        "Pressure Cooker", "Air Fryer", "Smoked", "Raw", "Fermented"
    ]

    # Ingredient categories with all subcategories
    ingredient_categories = [
        # Proteins
        "Beef", "Pork", "Chicken", "Turkey", "Fish", "Seafood", "Eggs", "Tofu",
        "Tempeh", "Seitan", "Legumes", "Game Meat", "Lamb", "Duck",
        
        # Dairy & Alternatives
        "Milk", "Cheese", "Yogurt", "Cream", "Butter", "Plant-Based Milk",
        "Vegan Cheese", "Sour Cream", "Cottage Cheese", "Ice Cream",
        
        # Vegetables
        "Leafy Greens", "Root Vegetables", "Tomatoes", "Peppers", "Onions",
        "Garlic", "Mushrooms", "Potatoes", "Carrots", "Broccoli", "Cauliflower",
        "Squash", "Zucchini", "Eggplant", "Cabbage", "Brussels Sprouts",
        "Sweet Potatoes", "Corn", "Peas", "Green Beans", "Asparagus", "Artichokes",
        
        # Fruits
        "Citrus Fruits", "Berries", "Stone Fruits", "Tropical Fruits", "Apples",
        "Pears", "Grapes", "Melons", "Bananas", "Dried Fruits", "Exotic Fruits",
        
        # Grains & Pasta
        "Rice", "Pasta", "Bread", "Flour", "Cereals", "Quinoa", "Oats",
        "Barley", "Couscous", "Noodles", "Tortillas", "Breadcrumbs",
        
        # Pantry Items
        "Oils", "Vinegars", "Sauces", "Condiments", "Spices", "Herbs",
        "Nuts", "Seeds", "Dried Fruits", "Canned Vegetables", "Canned Fruits",
        "Canned Beans", "Canned Fish", "Broths", "Stocks", "Bouillon",
        
        # Baking
        "Baking Powder", "Baking Soda", "Yeast", "Sugar", "Brown Sugar",
        "Powdered Sugar", "Honey", "Maple Syrup", "Chocolate", "Cocoa Powder",
        "Vanilla Extract", "Food Coloring", "Decorating Items",
        
        # Seasonings & Spices
        "Salt", "Pepper", "Herbs", "Ground Spices", "Whole Spices", "Spice Blends",
        "Marinades", "Rubs", "Hot Sauces", "Curry Pastes", "Seasoning Mixes",
        
        # International Ingredients
        "Asian Ingredients", "Mexican Ingredients", "Italian Ingredients",
        "Indian Ingredients", "Middle Eastern Ingredients", "Mediterranean Ingredients"
    ]

    print("Starting to populate categories...")
    
    with app.app_context():
        try:
            # Add recipe categories directly using SQL
            with db.engine.connect() as conn:
                for cat_name in recipe_categories:
                    # Check if category exists
                    result = conn.execute(
                        text("SELECT id FROM category WHERE name = :name"),
                        {"name": cat_name}
                    )
                    if not result.first():
                        conn.execute(
                            text("INSERT INTO category (name) VALUES (:name)"),
                            {"name": cat_name}
                        )
                        print(f"Added recipe category: {cat_name}")
                conn.commit()
                
                # Add ingredient categories
                for ing_name in ingredient_categories:
                    # Check if ingredient category exists
                    result = conn.execute(
                        text("SELECT id FROM ingredient_category WHERE name = :name"),
                        {"name": ing_name}
                    )
                    if not result.first():
                        conn.execute(
                            text("INSERT INTO ingredient_category (name) VALUES (:name)"),
                            {"name": ing_name}
                        )
                        print(f"Added ingredient category: {ing_name}")
                conn.commit()
                
                # Print counts
                result = conn.execute(text("SELECT COUNT(*) FROM category"))
                recipe_count = result.scalar()
                
                result = conn.execute(text("SELECT COUNT(*) FROM ingredient_category"))
                ingredient_count = result.scalar()
                
                print(f"\nCurrent category counts in database:")
                print(f"Recipe categories: {recipe_count}")
                print(f"Ingredient categories: {ingredient_count}")
                
                # Print all categories
                print("\nAll Recipe Categories in database:")
                result = conn.execute(text("SELECT name FROM category ORDER BY name"))
                for row in result:
                    print(f"- {row[0]}")
                
                print("\nAll Ingredient Categories in database:")
                result = conn.execute(text("SELECT name FROM ingredient_category ORDER BY name"))
                for row in result:
                    print(f"- {row[0]}")
            
            return True
            
        except Exception as e:
            print(f"Error populating categories: {e}")
            return False

if __name__ == "__main__":
    populate_categories()