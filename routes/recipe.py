from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Recipe
from extensions import db

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/recipes')
@login_required
def list_recipes():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('recipe/list.html', recipes=recipes)

@recipe_bp.route('/recipe/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # Handle recipe creation later
        pass
    return render_template('recipe/create.html') 