from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class ShoppingListForm(FlaskForm):
    name = StringField('List Name', validators=[DataRequired(), Length(min=1, max=100)])
    recipes = SelectMultipleField('Recipes', coerce=int) 