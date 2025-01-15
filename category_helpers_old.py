from collections import defaultdict
from typing import Dict, List

from recipe_categories import RECIPE_CATEGORIES


class CategoryHelper:
    def __init__(self, categories: Dict = RECIPE_CATEGORIES):
        self.categories = categories
        self.flat_categories = {}
        self._flatten_categories()

    def _flatten_categories(self, d: Dict = None, parent: str = '') -> None:
        """Recursively flatten nested categories into a searchable format"""
        if d is None:
            d = self.categories

        for key, value in d.items():
            full_path = f"{parent}/{key}" if parent else key
            self.flat_categories[full_path] = []

            if isinstance(value, dict):
                self._flatten_categories(value, full_path)
            elif isinstance(value, list):
                self.flat_categories[full_path].extend(value)

    def get_main_categories(self) -> List[str]:
        """Get top-level categories"""
        return list(self.categories.keys())

    def get_subcategories(self, category_path: str) -> List[str]:
        """Get immediate subcategories of a given category path"""
        current = self.categories
        if category_path:
            for part in category_path.split('/'):
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return []

        if isinstance(current, dict):
            return list(current.keys())
        return []

    def get_recipes_in_category(self, category_path: str) -> List[str]:
        """Get recipes directly under a category"""
        return self.flat_categories.get(category_path, [])

    def search_recipes(self, query: str) -> Dict[str, List[str]]:
        """Search for recipes across all categories"""
        results = defaultdict(list)
        query = query.lower()

        for category, recipes in self.flat_categories.items():
            matching_recipes = [r for r in recipes if query in r.lower()]
            if matching_recipes:
                results[category].extend(matching_recipes)

        return dict(results)

    def get_category_path(self, recipe_name: str) -> List[str]:
        """Find all category paths containing a specific recipe"""
        paths = []
        for category, recipes in self.flat_categories.items():
            if recipe_name in recipes:
                paths.append(category)
        return paths

    def get_breadcrumb(self, category_path: str) -> List[str]:
        """Convert a category path to a list of breadcrumb items"""
        return category_path.split('/')

    def suggest_categories(self, recipe_name: str, ingredients: List[str]) -> List[str]:
        """Suggest appropriate categories based on recipe name and ingredients"""
        suggestions = set()
        recipe_name = recipe_name.lower()

        # Check recipe name against all category keywords
        for category, recipes in self.flat_categories.items():
            for recipe in recipes:
                if any(word in recipe_name for word in recipe.lower().split()):
                    suggestions.add(category)

        # Check ingredients against category keywords
        for ingredient in ingredients:
            ingredient = ingredient.lower()
            for category, recipes in self.flat_categories.items():
                if any(ingredient in recipe.lower() for recipe in recipes):
                    suggestions.add(category)

        return list(suggestions)


# Example usage functions
def create_category_select(categories: Dict, level: int = 0) -> List[tuple]:
    """Create a flat list of categories for select fields"""
    options = []
    prefix = "-- " * level

    for key, value in categories.items():
        options.append((key, f"{prefix}{key}"))
        if isinstance(value, dict):
            options.extend(create_category_select(value, level + 1))

    return options


def format_recipe_count(category_helper: CategoryHelper) -> Dict[str, int]:
    """Count recipes in each category"""
    counts = {}
    for category in category_helper.flat_categories:
        counts[category] = len(category_helper.get_recipes_in_category(category))
    return counts
