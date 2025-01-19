from flask_login import current_user, login_required, logout_user
from sqlalchemy import desc
from flask import Blueprint, render_template, current_app,request,redirect, url_for, flash, session, jsonify
from models.models import Recipe, Category, User
from forms.forms import RecipeForm, EditRecipeForm, EditUserForm
from extensions import db
from werkzeug.utils import secure_filename
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user

main_bp = Blueprint('main', __name__)

# Add this function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main_bp.route('/')
def index():
    try:
        recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
        featured_recipes = Recipe.query.limit(6).all()
        recipes = Recipe.query.limit(6).all()
        categories = Category.query.all()

        return render_template('home.html',
                           recipes=recipes,
                           categories=categories,
                           featured_recipes=featured_recipes,
                           recent_recipes=recent_recipes)
    except Exception as e:
        current_app.logger.error(f"Error fetching recipes: {e}")
        return render_template('home.html',
                           recipes=[],
                           categories=[],
                           featured_recipes=[],
                           recent_recipes=[])

@main_bp.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    
    # Get categories for the dropdown
    categories = Category.query.all()
    form.category.choices = [(c.id, c.name) for c in categories]
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Handle file upload if there's an image
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    image_filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))

            recipe = Recipe(
                name=form.title.data,
                description=form.description.data,
                ingredients=form.ingredients.data,
                instructions=form.instructions.data,
                category_id=form.category.data,
                user_id=current_user.id,
                image=image_filename
            )
            db.session.add(recipe)
            db.session.commit()
            flash('Recipe added successfully!', 'success')
            return redirect(url_for('main.recipes'))
        except Exception as e:
            current_app.logger.error(f"Error adding recipe: {e}")
            flash('Error adding recipe. Please try again.', 'error')
            db.session.rollback()

    return render_template('recipes/add_recipe.html', form=form, categories=categories)

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
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

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
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.index'))

        flash('Invalid username or password', 'error')

    return render_template('auth/login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

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
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    recipe = Recipe.query.get_or_404(recipe_id)
    try:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    recipe = Recipe.query.get_or_404(recipe_id)
    form = EditRecipeForm(obj=recipe)
    
    if form.validate_on_submit():
        try:
            recipe.title = form.title.data
            recipe.description = form.description.data
            recipe.category_id = form.category.data
            recipe.instructions = form.instructions.data
            
            # Handle image update
            if form.image.data:
                if recipe.image:
                    # Delete old image
                    old_image = os.path.join(current_app.config['UPLOAD_FOLDER'], recipe.image)
                    if os.path.exists(old_image):
                        os.remove(old_image)
                
                filename = secure_filename(form.image.data.filename)
                form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                recipe.image = filename
            
            # Handle image deletion
            if request.form.get('delete_image') and recipe.image:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], recipe.image))
                recipe.image = None
            
            db.session.commit()
            flash('Recipe updated successfully!', 'success')
            return redirect(url_for('main.manage_recipes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating recipe: {str(e)}', 'error')
    
    return render_template('admin/edit_recipe.html', form=form, recipe=recipe)

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