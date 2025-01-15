from recipe_data import All_Ingredients, Recipe_Category


class CategoryHelper:
    def __init__(self):
        self.ingredients = All_Ingredients
        self.categories = Recipe_Category

    def get_ingredients(self):
        """Return all available ingredients"""
        return self.ingredients

    def get_categories(self):
        """Return all available categories"""
        return self.categories

    def suggest_category(self, ingredients):
        """Suggest categories based on ingredients"""
        suggestions = set()

        for ingredient in ingredients:
            ingredient = ingredient.lower()

            # Breakfast items
            if any(word in ingredient for word in ['breakfast', 'cereal', 'yogurt', 'smoothie']):
                suggestions.add('Breakfast & Brunch')

            # Appetizers
            if any(word in ingredient for word in ['soup', 'salad', 'dip', 'appetizer', 'snack', 'wings']):
                suggestions.add('Appetizers & Snacks')
                suggestions.add('Appetizers & Starters')

            # Main dishes
            if any(word in ingredient for word in ['beef', 'chicken', 'pork', 'fish', 'lamb', 'pasta']):
                suggestions.add('Main Dishes')
                suggestions.add('Main Courses')

            # Desserts
            if any(word in ingredient for word in ['cake', 'cookie', 'pie', 'dessert', 'sweet']):
                suggestions.add('Desserts')
                suggestions.add('Desserts & Baking')

            # Ethnic cuisine
            if any(word in ingredient for word in ['asian', 'italian', 'french', 'mediterranean', 'indian']):
                suggestions.add('World Cuisines')
                suggestions.add('Ethnic Cuisine')

            # Special diets
            if any(word in ingredient for word in ['vegan', 'vegetarian', 'keto', 'gluten-free']):
                suggestions.add('Special Diet')
                suggestions.add('Special Diets')

            # Baking
            if any(word in ingredient for word in ['bread', 'baking', 'pastry', 'dough']):
                suggestions.add('Baking')

            # Seasonal
            if any(word in ingredient for word in ['christmas', 'thanksgiving', 'holiday', 'seasonal']):
                suggestions.add('Seasonal')
                suggestions.add('Seasonal & Holiday')

            # Sauces & Condiments
            if any(word in ingredient for word in ['sauce', 'condiment', 'dressing']):
                suggestions.add('Sauces & Condiments')

        return list(suggestions)

    def get_ingredient_category(self, ingredient):
        """Get the primary category for a single ingredient"""
        suggestions = self.suggest_category([ingredient])
        return suggestions[0] if suggestions else None

    def filter_ingredients_by_category(self, category):
        """Return all ingredients that belong to a specific category"""
        return [ingredient for ingredient in self.ingredients
                if category in self.suggest_category([ingredient])]
