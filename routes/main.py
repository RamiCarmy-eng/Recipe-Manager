from flask import Blueprint, render_template, request
from models.models import Recipe, Category
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get featured recipes_images
    featured_recipes = Recipe.query.filter_by(
        is_featured=True, 
        is_hidden=False
    ).limit(6).all()
    
    # Get latest recipes_images
    latest_recipes = Recipe.query.filter_by(
        is_hidden=False
    ).order_by(desc(Recipe.created_at)).limit(12).all()
    
    # Get all categories
    categories = Category.query.all()
    
    return render_template('main/index.html',
                         featured_recipes=featured_recipes,
                         latest_recipes=latest_recipes,
                         categories=categories)

@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    recipe_query = Recipe.query.filter_by(is_hidden=False)
    
    if query:
        recipe_query = recipe_query.filter(Recipe.name.ilike(f'%{query}%'))
    
    if category:
        recipe_query = recipe_query.filter_by(category=category)
    
    recipes = recipe_query.order_by(desc(Recipe.created_at)).all()
    categories = Category.query.all()
    
    return render_template('main/search.html',
                         recipes=recipes,
                         query=query,
                         selected_category=category,
                         categories=categories)

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html') 