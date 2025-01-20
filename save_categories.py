import sqlite3
from app import create_app
from extensions import db

def save_categories():
    print("Saving categories to recipes.db...")
    
    try:
        # Connect to recipes.db
        conn = sqlite3.connect('instance/recipes.db')
        cursor = conn.cursor()
        
        # Create categories table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE
        )
        """)
        
        # Create ingredient_categories table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE
        )
        """)
        
        # Recipe categories - COMPLETE LIST
        Recipe_Category = ['Appetizers & Snacks', 'Appetizers & Starters', 'Baking', 'Beverages', 'Breakfast & Brunch',
                   'Desserts', 'Desserts & Baking', 'Ethnic Cuisine', 'Main Courses', 'Main Dishes',
                   'Preserves & Canning', 'Sauces & Condiments', 'Seasonal', 'Seasonal & Holiday', 'Side Dishes',
                   'Special Diet', 'Special Diets', 'Techniques & Methods', 'World Cuisines']

        # Ingredient categories - COMPLETE LIST
        All_Ingredients = ['Asian', 'Asian Noodles', 'Baked Appetizers', 'Bar Cookies', 'Bean & Lentil',
                   'Beef', 'Breads & Baking', 'Breakfast Meats', 'Cheese Plates', 'Cheesecakes',
                   'Chicken', 'Christmas', 'Chunky Soups', 'Classic', 'Clear Soups', 'Coffee',
                   'Cold Cereals', 'Cold Seafood', 'Cold Soups', 'Compliant Meals', 'Cream Pies', 'Cream Soups',
                   'Croissant Based', 'Dips & Spreads', 'Drop Cookies', 'Dry Heat', 'East African', 'East Asian',
                   'Easter', 'Easter dishes', 'Egg Dishes', 'Emulsified Sauces', 'European', 'Fall Produce',
                   'Fat-Based', 'Fermentation', 'Fermented Foods', 'Finger Foods', 'Fish', 'French',
                   'Fresh Juices', 'Fried Appetizers', 'Fruit Based', 'Fruit Dishes', 'Fruit Jams', 'Fruit Pies',
                   'Game Meats', 'Grain Salads', 'Green Salads', 'Griddle Favorites', 'Grilled', 'Grilling & BBQ',
                   'Healthy Options', 'Hot Cereals', 'Hot Chocolate', 'Iced Drinks', 'Italian', 'Italian Pasta',
                   'Keto Desserts', 'Keto Mains', 'Keto Sides', 'Knife Skills', 'Lamb', 'Latin',
                   'Latin American', 'Layer Cakes', 'Lebanese', 'Legume Based', 'Main Dishes', 'Mains',
                   'Mediterranean', 'Mixed Seafood', 'Mixing Methods', 'Modern', 'Moist Heat',
                   'Molecular Gastronomy', 'Mother Sauces', 'New Year', 'North African', 'North American',
                   'Other Cakes', 'Other Grains', 'Other Noodles', 'Pan Sauces', 'Persian', 'Pickled Vegetables',
                   'Picnic & Outdoor', 'Plant-Based Proteins', 'Pork', 'Potatoes', 'Poultry', 'Protein Salads',
                   'Quick Breads', 'Rice', 'Roasted', 'Sauces & Dressings', 'Sautéed', 'Savory', 'Shellfish',
                   'Sides', 'Smoking & Curing', 'Smoothie Bowls', 'Smoothies', 'Snacks', 'South Asian',
                   'Southeast Asian', 'Special Cakes', 'Special Occasion', 'Specialty', 'Specialty Breads',
                   'Specialty Cookies', 'Specialty Preserves', 'Spice Blends', 'Spreads', 'Spring Produce', 'Steamed',
                   'Stuffed Items', 'Summer Produce', 'Sweet', 'Table Condiments', 'Tarts', 'Tea', 'Thanksgiving',
                   'Tofu & Tempeh', 'Tomato Based', 'Turkish', 'Vegan Specific', 'Vegetable Mains',
                   'Vegetable Platters', 'Vegetable Salads', 'Vegetarian Mains', 'Virgin Classics',
                   'Wellness Drinks', 'West African', 'Whole30 Sides', 'Winter Comfort', 'Yeast Breads',
                   'Yogurt Dishes']
        
        # Save Recipe Categories
        print("\nSaving Recipe Categories:")
        for category in Recipe_Category:
            try:
                cursor.execute("INSERT INTO categories (name) VALUES (?)", (category,))
                print(f"Added recipe category: {category}")
            except sqlite3.IntegrityError:
                print(f"Recipe category already exists: {category}")
        
        # Save Ingredient Categories
        print("\nSaving Ingredient Categories:")
        for ingredient in All_Ingredients:
            try:
                cursor.execute("INSERT INTO ingredient_categories (name) VALUES (?)", (ingredient,))
                print(f"Added ingredient category: {ingredient}")
            except sqlite3.IntegrityError:
                print(f"Ingredient category already exists: {ingredient}")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("\nAll categories saved successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    save_categories() 