from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from forms.recipe import RecipeForm
from flask_login import login_required, current_user
from models.models import Recipe, Category, Ingredient
from extensions import db

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
@login_required
def index():
    recipes = Recipe.query.all()
    return render_template('recipes/index.html', recipes=recipes)

@recipe_bp.route('/recipes')
@login_required
def list_recipes():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('recipe/list.html', recipes=recipes)

@recipe_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # Handle recipe creation
        title = request.form.get('title')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        prep_time = request.form.get('prep_time')
        cook_time = request.form.get('cook_time')
        servings = request.form.get('servings')
        difficulty = request.form.get('difficulty')
        category_id = request.form.get('category_id')

        recipe = Recipe(
            title=title,
            description=description,
            instructions=instructions,
            prep_time=prep_time,
            cook_time=cook_time,
            servings=servings,
            difficulty=difficulty,
            category_id=category_id,
            user_id=current_user.id
        )

        db.session.add(recipe)
        db.session.commit()

        flash('Recipe created successfully!')
        return redirect(url_for('recipe.index'))

    categories = Category.query.all()
    return render_template('recipes/create.html', categories=categories)

@recipe_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            subcategory=form.subcategory.data,
            prep_time=form.prep_time.data,
            cook_time=form.cook_time.data,
            servings=form.servings.data,
            instructions=form.instructions.data,
            user_id=current_user.id
        )
        
        # Handle ingredients
        ingredients = request.form.getlist('ingredients[]')
        amounts = request.form.getlist('amounts[]')
        units = request.form.getlist('units[]')
        categories = request.form.getlist('ingredient_categories[]')

        for i in range(len(ingredients)):
            if ingredients[i].strip():
                ingredient = Ingredient(
                    name=ingredients[i],
                    amount=amounts[i],
                    unit=units[i],
                    category=categories[i]
                )
                recipe.ingredients.append(ingredient)

        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('recipe.list_recipes'))

    return render_template('recipes/add_recipe.html', form=form, title='Add Recipe')

@recipe_bp.route('/ingredients/search')
def search_ingredients():
    query = request.args.get('q', '')
    category_id = request.args.get('category_id')
    
    # Base query
    ingredients_query = Ingredient.query.filter(
        Ingredient.name.ilike(f'%{query}%')
    )
    
    # Add category filter if provided
    if category_id:
        ingredients_query = ingredients_query.filter(Ingredient.category_id == category_id)
    
    ingredients = ingredients_query.order_by(Ingredient.name).limit(10).all()
    
    return jsonify([{
        'id': i.id,
        'name': i.name,
        'category': i.category.name,
        'default_unit': i.default_unit
    } for i in ingredients])