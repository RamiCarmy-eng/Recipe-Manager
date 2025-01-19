from models.models import Category, Ingredient

class CategoryHelper:
    def get_available_ingredients(self):
        return Ingredient.query.all()

    def get_categories(self):
        return Category.query.all() 