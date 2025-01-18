from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from models import Category, IngredientCategory
from extensions import db

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories')
@login_required
def list_categories():
    recipe_categories = Category.query.all()
    ingredient_categories = IngredientCategory.query.all()
    return render_template('category/list.html', 
                         recipe_categories=recipe_categories,
                         ingredient_categories=ingredient_categories)

@category_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        category_type = request.form.get('type')
        
        if category_type == 'recipe':
            category = Category(name=name)
        else:
            category = IngredientCategory(name=name)
            
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('category.list_categories'))
    
    return render_template('category/add.html') 