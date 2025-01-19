from flask_login import current_user, login_required, logout_user
from sqlalchemy import desc
from flask import Blueprint, render_template, current_app,request,redirect, url_for, flash, session, jsonify, send_file
from models.models import Recipe, Category, User, Ingredient
from forms.forms import RecipeForm, EditRecipeForm, EditUserForm
from extensions import db
from werkzeug.utils import secure_filename
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user
from forms.auth import LoginForm
from datetime import datetime
import json
import csv
from io import StringIO

main_bp = Blueprint('main', __name__)

# Add this function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main_bp.route('/')
def index():
    return redirect(url_for('main.login'))

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Handle the contact form submission (e.g., send email, save to database)
        flash('Thank you for your message!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html')

@main_bp.route('/recipes')
@login_required
def recipes():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('recipes/recipes.html', recipes=recipes, title='All Recipes')

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

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Clear any existing session
    if current_user.is_authenticated:
        logout_user()
    
    form = LoginForm()
    print(form)
    print(dir(form))
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.recipes'))
        flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html', form=form, title='Login')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/manage-recipes')
@login_required
def manage_recipes():
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    recipes = Recipe.query.all()
    return render_template('admin/manage_recipes.html', recipes=recipes)

@main_bp.route('/manage-users')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@main_bp.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to delete this recipe.', 'danger')
        return redirect(url_for('main.recipes'))
    
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('main.recipes'))

@main_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        return jsonify({'error': 'Cannot delete admin user'}), 400
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe.', 'danger')
        return redirect(url_for('main.recipes'))
    
    form = RecipeForm(obj=recipe)
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name)]
    
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.instructions = form.instructions.data
        recipe.prep_time = form.prep_time.data
        recipe.cook_time = form.cook_time.data
        recipe.servings = form.servings.data
        recipe.difficulty = form.difficulty.data
        recipe.category_id = form.category.data
        recipe.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('main.view_recipe', recipe_id=recipe.id))
        
    return render_template('recipes/recipe_form.html', 
                         form=form, 
                         title='Edit Recipe')

@main_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    
    if form.validate_on_submit():
        try:
            user.username = form.username.data
            user.email = form.email.data
            user.role = form.role.data
            
            if form.new_password.data:
                user.password = generate_password_hash(form.new_password.data)
            
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('main.manage_users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
    
    return render_template('admin/edit_user.html', form=form, user=user)

@main_bp.route('/home')
@login_required
def home():
    return render_template('home.html', title='Welcome')

@main_bp.route('/categories')
@login_required
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('recipes/categories.html', categories=categories, title='Categories')

@main_bp.route('/recipe/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name)]
    
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            instructions=form.instructions.data,
            prep_time=form.prep_time.data,
            cook_time=form.cook_time.data,
            servings=form.servings.data,
            difficulty=form.difficulty.data,
            category_id=form.category.data,
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(recipe)
        db.session.commit()
        
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('main.recipes'))
        
    return render_template('recipes/recipe_form.html', 
                         form=form, 
                         title='Add Recipe')

@main_bp.route('/recipe/<int:recipe_id>')
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to view this recipe.', 'danger')
        return redirect(url_for('main.recipes'))
    return render_template('recipes/view_recipe.html', recipe=recipe)

@main_bp.route('/recipes/search')
@login_required
def search_recipes():
    query = request.args.get('q', '')
    category_id = request.args.get('category')
    difficulty = request.args.get('difficulty')
    
    recipes_query = Recipe.query
    
    if query:
        recipes_query = recipes_query.filter(
            Recipe.title.ilike(f'%{query}%') |
            Recipe.description.ilike(f'%{query}%')
        )
    
    if category_id:
        recipes_query = recipes_query.filter(Recipe.category_id == category_id)
        
    if difficulty:
        recipes_query = recipes_query.filter(Recipe.difficulty == difficulty)
    
    recipes = recipes_query.order_by(Recipe.title).all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify([{
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'image': r.image,
            'category': r.category.name,
            'difficulty': r.difficulty
        } for r in recipes])
    
    categories = Category.query.order_by(Category.name).all()
    difficulties = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    
    return render_template('recipes/search.html',
                         recipes=recipes,
                         categories=categories,
                         difficulties=difficulties,
                         query=query,
                         category_id=category_id,
                         difficulty=difficulty)

@main_bp.route('/recipe/<int:recipe_id>/ingredients', methods=['GET', 'POST'])
@login_required
def manage_ingredients(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this recipe.', 'danger')
        return redirect(url_for('main.recipes'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Clear existing ingredients
        recipe.ingredients = []
        
        # Add new ingredients
        for item in data.get('ingredients', []):
            ingredient = Ingredient(
                name=item['name'],
                amount=item['amount'],
                unit=item.get('unit', '')
            )
            recipe.ingredients.append(ingredient)
        
        db.session.commit()
        return jsonify({'success': True})
    
    return render_template('recipes/ingredients.html', recipe=recipe)

@main_bp.route('/recipes/export/<string:format_type>')
@login_required
def export_recipes(format_type):
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    
    if format_type == 'json':
        # Export as JSON
        recipes_data = []
        for recipe in recipes:
            recipes_data.append({
                'title': recipe.title,
                'description': recipe.description,
                'instructions': recipe.instructions,
                'prep_time': recipe.prep_time,
                'cook_time': recipe.cook_time,
                'servings': recipe.servings,
                'difficulty': recipe.difficulty,
                'category': recipe.category.name,
                'ingredients': [
                    {
                        'name': i.name,
                        'amount': i.amount,
                        'unit': i.unit
                    } for i in recipe.ingredients
                ]
            })
        
        return jsonify(recipes_data)
        
    elif format_type == 'csv':
        # Export as CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Title', 'Category', 'Description', 'Instructions', 
                        'Prep Time', 'Cook Time', 'Servings', 'Difficulty', 
                        'Ingredients'])
        
        # Write recipes
        for recipe in recipes:
            ingredients = '; '.join([f"{i.amount} {i.unit} {i.name}" 
                                   for i in recipe.ingredients])
            writer.writerow([
                recipe.title,
                recipe.category.name,
                recipe.description,
                recipe.instructions,
                recipe.prep_time,
                recipe.cook_time,
                recipe.servings,
                recipe.difficulty,
                ingredients
            ])
        
        output.seek(0)
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'recipes_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    
    return jsonify({'error': 'Invalid format'}), 400

@main_bp.route('/recipes/import', methods=['POST'])
@login_required
def import_recipes():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if not file.filename.endswith(('.json', '.csv')):
        return jsonify({'error': 'Invalid file format'}), 400
    
    try:
        if file.filename.endswith('.json'):
            data = json.load(file)
            for recipe_data in data:
                category = Category.query.filter_by(name=recipe_data['category']).first()
                if not category:
                    category = Category(name=recipe_data['category'])
                    db.session.add(category)
                    db.session.flush()
                
                recipe = Recipe(
                    title=recipe_data['title'],
                    description=recipe_data['description'],
                    instructions=recipe_data['instructions'],
                    prep_time=recipe_data['prep_time'],
                    cook_time=recipe_data['cook_time'],
                    servings=recipe_data['servings'],
                    difficulty=recipe_data['difficulty'],
                    category_id=category.id,
                    user_id=current_user.id,
                    created_at=datetime.utcnow()
                )
                
                for ingredient_data in recipe_data['ingredients']:
                    ingredient = Ingredient(
                        name=ingredient_data['name'],
                        amount=ingredient_data['amount'],
                        unit=ingredient_data.get('unit', '')
                    )
                    recipe.ingredients.append(ingredient)
                
                db.session.add(recipe)
        
        else:  # CSV file
            csv_data = csv.DictReader(StringIO(file.read().decode()))
            for row in csv_data:
                category = Category.query.filter_by(name=row['Category']).first()
                if not category:
                    category = Category(name=row['Category'])
                    db.session.add(category)
                    db.session.flush()
                
                recipe = Recipe(
                    title=row['Title'],
                    description=row['Description'],
                    instructions=row['Instructions'],
                    prep_time=int(row['Prep Time']),
                    cook_time=int(row['Cook Time']),
                    servings=int(row['Servings']),
                    difficulty=row['Difficulty'],
                    category_id=category.id,
                    user_id=current_user.id,
                    created_at=datetime.utcnow()
                )
                
                # Parse ingredients
                ingredients_text = row['Ingredients'].split(';')
                for ingredient_text in ingredients_text:
                    if ingredient_text.strip():
                        parts = ingredient_text.strip().split(' ', 2)
                        if len(parts) >= 3:
                            amount, unit, name = parts
                        else:
                            amount, name = parts
                            unit = ''
                        
                        ingredient = Ingredient(
                            name=name.strip(),
                            amount=amount.strip(),
                            unit=unit.strip()
                        )
                        recipe.ingredients.append(ingredient)
                
                db.session.add(recipe)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Recipes imported successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400