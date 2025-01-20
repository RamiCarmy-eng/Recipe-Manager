from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.models import Recipe, Category, Ingredient
from sqlalchemy import or_

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    category_id = request.args.get('category')

    recipe_query = Recipe.query.filter_by(is_hidden=False)

    if query:
        recipe_query = recipe_query.filter(
            or_(
                Recipe.title.ilike(f'%{query}%'),
                Recipe.description.ilike(f'%{query}%')
            )
        )

    if category_id:
        recipe_query = recipe_query.filter_by(category_id=category_id)

    recipes = recipe_query.order_by(Recipe.title).all()
    categories = Category.query.order_by(Category.name).all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify([{
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'category': r.category.name
        } for r in recipes])

    return render_template('search/results.html',
                           recipes=recipes,
                           categories=categories,
                           query=query)


@search_bp.route('/search/ingredients')
@login_required
def search_ingredients():
    query = request.args.get('q', '')
    ingredients = Ingredient.query.filter(
        Ingredient.name.ilike(f'%{query}%')
    ).limit(10).all()

    return jsonify([{
        'id': i.id,
        'name': i.name,
        'unit': i.default_unit
    } for i in ingredients])