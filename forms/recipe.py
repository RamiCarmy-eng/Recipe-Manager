from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

# Define your categories dictionary
categories = {
    'Breakfast & Brunch': ['Breakfast Meats', 'Classic', 'Cold Cereals', 'Croissant Based', 'Egg Dishes',
                          'Fruit Dishes', 'Griddle Favorites', 'Healthy Options', 'Hot Cereals', 'Savory',
                          'Smoothie Bowls', 'Sweet', 'Yogurt Dishes'],
    'Appetizers & Snacks': ['bisque', 'broth', 'chowder', 'coleslaw', 'green salad', 'guacamole', 'hummus',
                           'nachos', 'pasta salad', 'pate', 'potato salad', 'salsa', 'soup', 'spring rolls',
                           'tapas', 'wings'],
    # ... rest of your categories ...
}

RECIPE_CATEGORIES = [
    (cat, cat) for cat in [
        'Breakfast & Brunch', 'Appetizers & Snacks', 'Main Dishes', 'Side Dishes',
        'Desserts', 'Beverages', 'Ethnic Cuisine', 'Special Diet', 'Baking',
        'Seasonal', 'Appetizers & Starters', 'Main Courses', 'Desserts & Baking',
        'World Cuisines', 'Special Diets', 'Seasonal & Holiday', 'Preserves & Canning',
        'Sauces & Condiments', 'Techniques & Methods'
    ]
]

INGREDIENT_CATEGORIES = [
    (cat, cat) for cat in categories.keys()  # Using your categories dictionary
]

UNITS = [
    ('g', 'Grams'),
    ('kg', 'Kilograms'),
    ('ml', 'Milliliters'),
    ('l', 'Liters'),
    ('tsp', 'Teaspoon'),
    ('tbsp', 'Tablespoon'),
    ('cup', 'Cup'),
    ('piece', 'Piece'),
    ('to taste', 'To Taste')
]

class IngredientForm(FlaskForm):
    name = StringField('Ingredient Name', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    unit = SelectField('Unit', choices=UNITS)
    category = SelectField('Category', choices=[(cat, cat) for cat in categories.keys()])

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    prep_time = IntegerField('Preparation Time (minutes)', 
                            validators=[DataRequired(), NumberRange(min=1)])
    cook_time = IntegerField('Cooking Time (minutes)', 
                            validators=[DataRequired(), NumberRange(min=1)])
    servings = IntegerField('Servings', validators=[DataRequired(), NumberRange(min=1)])
    difficulty = SelectField('Difficulty', 
                           choices=[('easy', 'Easy'), 
                                  ('medium', 'Medium'), 
                                  ('hard', 'Hard')])
    category = SelectField('Category', coerce=int)
    image = FileField('Recipe Image', 
                     validators=[FileAllowed(['jpg', 'png', 'jpeg'], 
                                          'Images only!')]) 