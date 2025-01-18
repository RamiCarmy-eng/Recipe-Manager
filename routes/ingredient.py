from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from models import Ingredient, IngredientCategory
from extensions import db

ingredient_bp = Blueprint('ingredient', __name__)

@ingredient_bp.route('/ingredients')
@login_required
def list_ingredients():
    ingredients = Ingredient.query.all()
    categories = IngredientCategory.query.all()
    return render_template('ingredient/list.html', 
                         ingredients=ingredients,
                         categories=categories)

@ingredient_bp.route('/ingredients/add', methods=['GET', 'POST'])
@login_required
def add_ingredient():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        
        ingredient = Ingredient(name=name, description=description, category=category)
        db.session.add(ingredient)
        db.session.commit()
        return redirect(url_for('ingredient.list_ingredients'))
    
    return render_template('ingredient/add.html')
