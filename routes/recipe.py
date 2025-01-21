from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from forms.recipe import RecipeForm
from flask_login import login_required, current_user
from models.models import Recipe, Category, Ingredient, RecipeIngredient
from extensions import db
import os
from flask import current_app
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

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
    
    # Load categories for the dropdown
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by('name')]
    
    if form.validate_on_submit():
        # Create new recipe
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            prep_time=form.prep_time.data,
            cook_time=form.cook_time.data,
            difficulty=form.difficulty.data,
            category_id=form.category_id.data,
            user_id=current_user.id
        )
        
        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            if filename:
                # Ensure directory exists
                recipe_images_path = os.path.join(current_app.static_folder, 'recipe_images')
                if not os.path.exists(recipe_images_path):
                    os.makedirs(recipe_images_path)
                
                # Save the file
                image_path = os.path.join(recipe_images_path, filename)
                form.image.data.save(image_path)
                recipe.image_filename = filename

        # Add recipe to database
        db.session.add(recipe)
        db.session.flush()  # Get recipe ID

        # Handle ingredients
        ingredient_index = 0
        while True:
            name = request.form.get(f'ingredient_name_{ingredient_index}')
            if not name:
                break
                
            amount = request.form.get(f'ingredient_amount_{ingredient_index}')
            unit = request.form.get(f'ingredient_unit_{ingredient_index}')

            # Get or create ingredient
            ingredient = Ingredient.query.filter_by(name=name).first()
            if not ingredient:
                ingredient = Ingredient(name=name)
                db.session.add(ingredient)
                db.session.flush()

            # Create recipe ingredient relationship
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                amount=float(amount) if amount else None,
                unit=unit
            )
            db.session.add(recipe_ingredient)
            
            ingredient_index += 1

        db.session.commit()
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe.id))

    return render_template('recipes/add_recipe.html', 
                         form=form, 
                         title='Add New Recipe')

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if user is authorized to edit
    if recipe.user_id != current_user.id:
        flash('You can only edit your own recipes.', 'error')
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe_id))
    
    form = RecipeForm(obj=recipe)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by('name')]
    
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.prep_time = form.prep_time.data
        recipe.cook_time = form.cook_time.data
        recipe.difficulty = form.difficulty.data
        recipe.category_id = form.category_id.data
        
        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            if filename:
                # Remove old image if exists
                if recipe.image_filename:
                    old_image_path = os.path.join(current_app.static_folder, 'recipe_images', recipe.image_filename)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                # Save new image
                image_path = os.path.join(current_app.static_folder, 'recipe_images', filename)
                form.image.data.save(image_path)
                recipe.image_filename = filename

        # Update ingredients
        # First remove all existing ingredients
        RecipeIngredient.query.filter_by(recipe_id=recipe.id).delete()
        
        # Add new ingredients
        ingredient_index = 0
        while True:
            name = request.form.get(f'ingredient_name_{ingredient_index}')
            if not name:
                break
                
            amount = request.form.get(f'ingredient_amount_{ingredient_index}')
            unit = request.form.get(f'ingredient_unit_{ingredient_index}')

            ingredient = Ingredient.query.filter_by(name=name).first()
            if not ingredient:
                ingredient = Ingredient(name=name)
                db.session.add(ingredient)
                db.session.flush()

            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                amount=float(amount) if amount else None,
                unit=unit
            )
            db.session.add(recipe_ingredient)
            
            ingredient_index += 1

        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe.id))

    # Pre-populate ingredients for editing
    if request.method == 'GET':
        return render_template('recipes/add_recipe.html',
                            form=form,
                            recipe=recipe,
                            title='Edit Recipe')

    return render_template('recipes/add_recipe.html',
                         form=form,
                         title='Edit Recipe')

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

@recipe_bp.route('/<int:recipe_id>')
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.options(
        joinedload(Recipe.category),
        joinedload(Recipe.recipe_ingredients)
    ).get_or_404(recipe_id)
    
    # Update image path to use /static/images/
    recipe_images_path = os.path.join(current_app.static_folder, 'images')
    if not os.path.exists(recipe_images_path):
        os.makedirs(recipe_images_path)
    
    # Check if image exists
    if recipe.image_filename:
        image_path = os.path.join(recipe_images_path, recipe.image_filename)
        if not os.path.exists(image_path):
            recipe.image_filename = None
    
    return render_template('recipes/recipe.html', 
                         recipe=recipe, 
                         title=recipe.name)

@recipe_bp.route('/<int:recipe_id>/ingredients')
@login_required
def recipe_ingredients(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    ingredients = db.session.query(
        RecipeIngredient, 
        Ingredient
    ).join(
        Ingredient, 
        RecipeIngredient.ingredient_id == Ingredient.id
    ).filter(
        RecipeIngredient.recipe_id == recipe_id
    ).all()
    
    return render_template('recipes/ingredients.html',
                         recipe=recipe,
                         ingredients=ingredients)