from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, FieldList, FormField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Optional

class IngredientForm(FlaskForm):
    name = StringField('Ingredient Name', validators=[DataRequired()])
    amount = StringField('Amount')
    unit = StringField('Unit')

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=6)])

class EditRecipeForm(RecipeForm):
    def __init__(self, *args, **kwargs):
        super(EditRecipeForm, self).__init__(*args, **kwargs)
        self.original_title = kwargs.get('obj', None) and kwargs['obj'].title
