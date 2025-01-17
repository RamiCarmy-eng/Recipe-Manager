# Standard library imports
import csv
import io
import json
import os
import re
import sqlite3
import threading
import time
import uuid
from datetime import datetime
from functools import wraps

# Third-party imports
from PIL import Image
import click
from flask import (
    Flask, render_template, request, redirect, send_from_directory,
    url_for, flash, session, abort, send_file, jsonify, g
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Local imports
from extensions import db, login_manager
from utils.category_helpers import CategoryHelper
from config import Config, AppConfig

# Model imports - all in one place
from models import (
    User, Recipe, Ingredient, Category,
    Favorite, Comment, RecipeIngredient,
    ShoppingList, ShoppingListItem
)
# Create Flask app
app = Flask(__name__)
app.config.from_object(AppConfig)

# Configuration
app.config.update(
    # Database configuration
    SQLALCHEMY_DATABASE_URI='sqlite:///instance/recipes.db',  # Updated path
    SQLALCHEMY_TRACK_MODIFICATIONS=False,

    # Security configuration
    SECRET_KEY='dev',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',

    # File upload configuration
    UPLOAD_FOLDER=os.path.join('static', 'uploads'),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'},

    # Admin configuration
    ADMIN_USERNAME='admin',
    ADMIN_PASSWORD='admin123'
)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create category helper instance
helper = CategoryHelper()
login_manager.init_app(app)


# Create tables within application context
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))

        # Create admin user if not exists
        admin = get_user_by_username(app.config['ADMIN_USERNAME'])
        if not admin:
            db.execute(
                'INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)',
                (app.config['ADMIN_USERNAME'],
                 generate_password_hash(app.config['ADMIN_PASSWORD']),
                 'admin',
                 datetime.now())
            )
            db.commit()


# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check Flask-Login authentication
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

        # Then check session (as backup)
        if 'user_id' not in session:
            return redirect(url_for('login'))

        # Check both current_user and session for admin role
        if not current_user.is_admin() or session.get('role') != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            abort(403)  # Forbidden

        return f(*args, **kwargs)

    return decorated_function

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_user_by_id(user_id):
    return db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()


def get_user_by_username(username):
    return db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()


def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        # Resize and save image
        img = Image.open(file)
        img.thumbnail((800, 800))
        img.save(filepath, optimize=True, quality=85)

        return unique_filename
    return None


def delete_image(filename):
    if filename:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)


def format_datetime(value):
    if value is None:
        return ""
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')


app.jinja_env.filters['datetime'] = format_datetime

"""# Authentication routes
@app.route('/')
def index():
    return redirect(url_for('login'))"""


# Home route
@app.route('/')
def home():
    try:
        recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
    except Exception as e:
        recent_recipes = []
        app.logger.error(f"Error fetching recipes: {e}")

    return render_template('home.html', recent_recipes=recent_recipes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Flask-Login
            login_user(user)

            # Session
            session['user_id'] = user.id
            session['role'] = user.role

            flash('Login successful!', 'success')
            return redirect(url_for('home'))

        flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        # Validation
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif get_user_by_username(username) is not None:
            error = f'User {username} is already registered.'

        if error is None:
            try:
                db.execute(
                    '''INSERT INTO users 
                       (username, password, role, created_at) 
                       VALUES (?, ?, ?, ?)''',
                    (username,
                     generate_password_hash(password),
                     'user',
                     datetime.now())
                )
                db.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))

            except sqlite3.Error as e:
                error = f'Database error: {e}'
                db.rollback()

        flash(error, 'danger')

    return render_template('register.html')


@app.route('/debug/schema')
def show_schema():
    if not app.debug:
        abort(404)
    schema = db.execute('PRAGMA table_info(users)').fetchall()
    return {'schema': [dict(column) for column in schema]}


# Recipe Management Routes
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.template_filter('nl2br')
def nl2br(value):
    return value.replace('\n', '<br>\n') if value else ''

@app.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        category = request.form.get('category')
        ingredients = request.form.getlist('ingredients[]')
        amounts = request.form.getlist('amounts[]')
        units = request.form.getlist('units[]')
        image = request.files.get('image')

        error = None

        if not name:
            error = 'Name is required.'
        elif not instructions:
            error = 'Instructions are required.'
        elif not ingredients:
            error = 'At least one ingredient is required.'

        if error is None:
            try:
                # Save image if provided
                image_filename = save_image(image) if image else None

                # Insert recipe
                cursor = db.execute(
                    '''INSERT INTO recipes 
                       (name, description, instructions, category, image, user_id, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (name, description, instructions, category, image_filename,
                     session['user_id'], datetime.now())
                )
                recipe_id = cursor.lastrowid

                # Insert ingredients
                for i, ingredient in enumerate(ingredients):
                    if ingredient.strip():  # Only insert non-empty ingredients
                        db.execute(
                            '''INSERT INTO recipe_ingredients 
                               (recipe_id, name, amount, unit)
                               VALUES (?, ?, ?, ?)''',
                            (recipe_id, ingredient, amounts[i], units[i])
                        )

                db.commit()
                return redirect(url_for('view_recipe', id=recipe_id))

            except sqlite3.Error as e:
                error = f"Database error: {e}"
                if image_filename:
                    delete_image(image_filename)

        flash(error)

    return render_template('recipe_form.html')


@app.route('/recipe/<int:id>')
@login_required
def view_recipe(id):
    # Get recipe with all details
    recipe = db.execute('''
        SELECT r.*, u.username as author
        FROM recipes r
        JOIN users u ON r.user_id = u.id
        WHERE r.id = ?
    ''', [id]).fetchone()

    if not recipe:
        abort(404)

    # Get ingredients
    ingredients = db.execute('''
        SELECT ri.*, i.name
        FROM recipe_ingredients ri
        JOIN ingredients i ON ri.ingredient_id = i.id
        WHERE ri.recipe_id = ?
    ''', [id]).fetchall()

    # Get comments with authors
    comments = db.execute('''
        SELECT c.*, u.username as author
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.recipe_id = ?
        ORDER BY c.created_at DESC
    ''', [id]).fetchall()

    # Check if user has favorited
    favorite = db.execute('''
        SELECT 1 FROM favorites
        WHERE user_id = ? AND recipe_id = ?
    ''', [session['user_id'], id]).fetchone()

    # Get favorite count
    favorite_count = db.execute('''
        SELECT COUNT(*) as count
        FROM favorites
        WHERE recipe_id = ?
    ''', [id]).fetchone()['count']

    return render_template('recipe.html',
                           recipe=recipe,
                           ingredients=ingredients,
                           comments=comments,
                           is_favorite=favorite is not None,
                           favorite_count=favorite_count)

@app.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = db.execute(
        'SELECT * FROM recipes WHERE id = ? AND user_id = ?',
        (id, session['user_id'])
    ).fetchone()

    if recipe is None:
        abort(403)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        category = request.form.get('category')
        ingredients = request.form.getlist('ingredients[]')
        amounts = request.form.getlist('amounts[]')
        units = request.form.getlist('units[]')
        image = request.files.get('image')

        error = None

        if not name:
            error = 'Name is required.'
        elif not instructions:
            error = 'Instructions are required.'
        elif not ingredients:
            error = 'At least one ingredient is required.'

        if error is None:
            try:
                # Handle image update
                image_filename = recipe['image']
                if image:
                    new_image = save_image(image)
                    if new_image:
                        delete_image(image_filename)
                        image_filename = new_image

                # Update recipe
                db.execute(
                    '''UPDATE recipes 
                       SET name = ?, description = ?, instructions = ?,
                           category = ?, image = ?, updated_at = ?
                       WHERE id = ?''',
                    (name, description, instructions, category,
                     image_filename, datetime.now(), id)
                )

                # Update ingredients
                db.execute('DELETE FROM recipe_ingredients WHERE recipe_id = ?', (id,))
                for i, ingredient in enumerate(ingredients):
                    if ingredient.strip():
                        db.execute(
                            '''INSERT INTO recipe_ingredients 
                               (recipe_id, name, amount, unit)
                               VALUES (?, ?, ?, ?)''',
                            (id, ingredient, amounts[i], units[i])
                        )

                db.commit()
                return redirect(url_for('view_recipe', id=id))

            except sqlite3.Error as e:
                error = f"Database error: {e}"

        flash(error)

    ingredients = db.execute(
        'SELECT * FROM recipe_ingredients WHERE recipe_id = ?',
        (id,)
    ).fetchall()

    return render_template('recipe_form.html', recipe=recipe, ingredients=ingredients)


@app.route('/recipe/<int:id>/delete', methods=['POST'])
@login_required
def delete_recipe(id):

    recipe = db.execute(
        'SELECT * FROM recipes WHERE id = ? AND user_id = ?',
        (id, session['user_id'])
    ).fetchone()

    if recipe is None:
        abort(403)

    try:
        # Delete image if exists
        if recipe['image']:
            delete_image(recipe['image'])

        # Delete recipe and related data
        db.execute('DELETE FROM recipe_ingredients WHERE recipe_id = ?', (id,))
        db.execute('DELETE FROM favorites WHERE recipe_id = ?', (id,))
        db.execute('DELETE FROM comments WHERE recipe_id = ?', (id,))
        db.execute('DELETE FROM recipes WHERE id = ?', (id,))
        db.commit()

        flash('Recipe deleted successfully.')
        return redirect(url_for('recipes'))

    except sqlite3.Error as e:
        db.rollback()
        flash(f'Error deleting recipe: {e}')
        return redirect(url_for('view_recipe', id=id))


# Shopping List Management
@app.route('/shopping-list')
@login_required
def shopping_list():

    items = db.execute('''
        SELECT sl.*, r.name as recipe_name 
        FROM shopping_list sl
        LEFT JOIN recipes r ON sl.recipe_id = r.id
        WHERE sl.user_id = ?
        ORDER BY sl.category, sl.name
    ''', (session['user_id'],)).fetchall()
    return render_template('shopping_list.html', items=items)


@app.route('/shopping-list/add', methods=['POST'])
@login_required
def add_to_shopping_list():
    name = request.form.get('name')
    amount = request.form.get('amount')
    unit = request.form.get('unit')
    category = request.form.get('category')
    recipe_id = request.form.get('recipe_id')

    if not name:
        flash('Item name is required.')
        return redirect(url_for('shopping_list'))


    try:
        db.execute('''
            INSERT INTO shopping_list (name, amount, unit, category, recipe_id, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, amount, unit, category, recipe_id, session['user_id']))
        db.commit()
        flash('Item added to shopping list.')
    except sqlite3.Error as e:
        flash(f'Error adding item: {e}')

    return redirect(url_for('shopping_list'))


@app.route('/shopping-list/<int:id>/delete', methods=['POST'])
@login_required
def remove_from_shopping_list(id):
    db.execute('DELETE FROM shopping_list WHERE id = ? AND user_id = ?',
               (id, session['user_id']))
    db.commit()
    return redirect(url_for('shopping_list'))


@app.route('/shopping-list/clear', methods=['POST'])
@login_required
def clear_shopping_list():

    db.execute('DELETE FROM shopping_list WHERE user_id = ?', (session['user_id'],))
    db.commit()
    return redirect(url_for('shopping_list'))


# Meal Planning
@app.route('/meal-plan')
@login_required
def meal_plan():
    start_date = request.args.get('start_date', datetime.now().strftime('%Y-%m-%d'))

    meals = db.execute('''
        SELECT mp.*, r.name as recipe_name, r.image as recipe_image
        FROM meal_plan mp
        LEFT JOIN recipes r ON mp.recipe_id = r.id
        WHERE mp.user_id = ? AND mp.date >= ?
        ORDER BY mp.date, mp.meal_type
    ''', (session['user_id'], start_date)).fetchall()
    return render_template('meal_plan.html', meals=meals, start_date=start_date)


@app.route('/meal-plan/add', methods=['POST'])
@login_required
def add_to_meal_plan():
    date = request.form.get('date')
    meal_type = request.form.get('meal_type')
    recipe_id = request.form.get('recipe_id')

    if not all([date, meal_type, recipe_id]):
        flash('All fields are required.')
        return redirect(url_for('meal_plan'))


    try:
        db.execute('''
            INSERT INTO meal_plan (date, meal_type, recipe_id, user_id)
            VALUES (?, ?, ?, ?)
        ''', (date, meal_type, recipe_id, session['user_id']))
        db.commit()
        flash('Meal added to plan.')
    except sqlite3.Error as e:
        flash(f'Error adding meal: {e}')

    return redirect(url_for('meal_plan'))


# Admin Routes
@app.route('/admin')
@admin_required
def admin_dashboard():

    total_users = db.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    total_recipes = db.execute('SELECT COUNT(*) as count FROM recipes').fetchone()['count']
    recent_users = db.execute(
        'SELECT * FROM users ORDER BY created_at DESC LIMIT 5'
    ).fetchall()
    recent_recipes = db.execute(
        'SELECT r.*, u.username FROM recipes r JOIN users u ON r.user_id = u.id ORDER BY r.created_at DESC LIMIT 5'
    ).fetchall()

    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_recipes=total_recipes,
                           recent_users=recent_users,
                           recent_recipes=recent_recipes)


@app.route('/admin/users')
@admin_required
def admin_users():

    users = db.execute('SELECT * FROM users ORDER BY username').fetchall()
    return render_template('admin/users.html', users=users)


@app.route('/admin/user/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(id):
    user = db.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if user is None:
        abort(404)

    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        password = request.form.get('password')

        error = None

        if not username:
            error = 'Username is required.'

        if error is None:
            try:
                if password:
                    db.execute('''
                        UPDATE users 
                        SET username = ?, role = ?, password = ?
                        WHERE id = ?
                    ''', (username, role, generate_password_hash(password), id))
                else:
                    db.execute('''
                        UPDATE users 
                        SET username = ?, role = ?
                        WHERE id = ?
                    ''', (username, role, id))
                db.commit()
                flash('User updated successfully.')
                return redirect(url_for('admin_users'))
            except sqlite3.Error as e:
                error = f'Database error: {e}'

        flash(error)

    return render_template('admin/user_form.html', user=user)


@app.route('/api/recipe/<int:id>/favorite', methods=['POST'])
@login_required
def api_toggle_favorite(id):

    favorite = db.execute('''
        SELECT * FROM favorites 
        WHERE user_id = ? AND recipe_id = ?
    ''', (session['user_id'], id)).fetchone()

    if favorite:
        db.execute('''
            DELETE FROM favorites 
            WHERE user_id = ? AND recipe_id = ?
        ''', (session['user_id'], id))
        is_favorite = False
    else:
        db.execute('''
            INSERT INTO favorites (user_id, recipe_id)
            VALUES (?, ?)
        ''', (session['user_id'], id))
        is_favorite = True

    db.commit()
    return jsonify({'success': True, 'is_favorite': is_favorite})


# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def internal_error(error):

    db.rollback()
    return render_template('errors/500.html'), 500


# CLI Commands
@app.cli.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# User Management Routes
@app.route('/users')
@admin_required
def manage_users():

    users = db.execute('''
        SELECT u.*, 
               COUNT(DISTINCT r.id) as recipe_count,
               COUNT(DISTINCT f.id) as favorite_count,
               MAX(r.created_at) as last_recipe_date
        FROM users u
        LEFT JOIN recipes r ON u.id = r.user_id
        LEFT JOIN favorites f ON u.id = f.user_id
        GROUP BY u.id
        ORDER BY u.username
    ''').fetchall()
    return render_template('admin/users.html', users=users)


def is_admin():
    """Check if current user is an admin."""
    if 'user_id' not in session:
        return False

    user = get_user_by_id(session['user_id'])
    return user and user['role'] == 'admin'


@app.route('/user/<int:id>/profile', methods=['GET', 'POST'])
@login_required
def user_profile(id):
    if id != session['user_id'] and not is_admin():
        abort(403)


    user = db.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if user is None:
        abort(404)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        avatar = request.files.get('avatar')

        error = None

        # Validate username
        if not username:
            error = 'Username is required.'
        elif username != user['username'] and get_user_by_username(username):
            error = 'Username already taken.'

        # Validate email format
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error = 'Invalid email address.'

        # Handle password change
        if new_password:
            if not current_password:
                error = 'Current password is required to set new password.'
            elif not check_password_hash(user['password'], current_password):
                error = 'Incorrect current password.'

        if error is None:
            try:
                # Handle avatar upload
                avatar_filename = user['avatar']
                if avatar:
                    new_avatar = save_image(avatar)
                    if new_avatar:
                        delete_image(avatar_filename)
                        avatar_filename = new_avatar

                # Update user information
                if new_password:
                    db.execute('''
                        UPDATE users 
                        SET username = ?, email = ?, password = ?, 
                            avatar = ?, updated_at = ?
                        WHERE id = ?
                    ''', (username, email, generate_password_hash(new_password),
                          avatar_filename, datetime.now(), id))
                else:
                    db.execute('''
                        UPDATE users 
                        SET username = ?, email = ?, avatar = ?, 
                            updated_at = ?
                        WHERE id = ?
                    ''', (username, email, avatar_filename,
                          datetime.now(), id))

                db.commit()
                flash('Profile updated successfully.')
                return redirect(url_for('user_profile', id=id))

            except sqlite3.Error as e:
                error = f'Database error: {e}'

        flash(error)

    # Get user statistics
    stats = db.execute('''
        SELECT 
            COUNT(DISTINCT r.id) as recipe_count,
            COUNT(DISTINCT f.id) as favorite_count,
            COUNT(DISTINCT c.id) as comment_count,
            MAX(r.created_at) as last_recipe_date
        FROM users u
        LEFT JOIN recipes r ON u.id = r.user_id
        LEFT JOIN favorites f ON u.id = f.user_id
        LEFT JOIN comments c ON u.id = c.user_id
        WHERE u.id = ?
    ''', (id,)).fetchone()

    # Get user's recent activity
    recent_recipes = db.execute('''
        SELECT * FROM recipes 
        WHERE user_id = ?
        ORDER BY created_at DESC LIMIT 5
    ''', (id,)).fetchall()

    recent_favorites = db.execute('''
        SELECT r.*, f.created_at as favorited_at
        FROM recipes r
        JOIN favorites f ON r.id = f.recipe_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC LIMIT 5
    ''', (id,)).fetchall()

    recent_comments = db.execute('''
        SELECT c.*, r.name as recipe_name
        FROM comments c
        JOIN recipes r ON c.recipe_id = r.id
        WHERE c.user_id = ?
        ORDER BY c.created_at DESC LIMIT 5
    ''', (id,)).fetchall()

    return render_template('user/profile.html',
                           user=user,
                           stats=stats,
                           recent_recipes=recent_recipes,
                           recent_favorites=recent_favorites,
                           recent_comments=recent_comments)


@app.route('/user/<int:id>/delete', methods=['POST'])
@admin_required
def delete_user(id):
    if id == session['user_id']:
        flash('Cannot delete your own account.')
        return redirect(url_for('manage_users'))


    user = db.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if user is None:
        abort(404)

    try:
        # Delete user's avatar if exists
        if user['avatar']:
            delete_image(user['avatar'])

        # Delete user's recipe images
        recipes = db.execute('SELECT image FROM recipes WHERE user_id = ?', (id,)).fetchall()
        for recipe in recipes:
            if recipe['image']:
                delete_image(recipe['image'])

        # Delete user's data
        db.execute('DELETE FROM comments WHERE user_id = ?', (id,))
        db.execute('DELETE FROM favorites WHERE user_id = ?', (id,))
        db.execute('DELETE FROM shopping_list WHERE user_id = ?', (id,))
        db.execute('DELETE FROM meal_plan WHERE user_id = ?', (id,))
        db.execute('DELETE FROM recipes WHERE user_id = ?', (id,))
        db.execute('DELETE FROM users WHERE id = ?', (id,))
        db.commit()

        flash('User and all associated data deleted successfully.')

    except sqlite3.Error as e:
        db.rollback()
        flash(f'Error deleting user: {e}')

    return redirect(url_for('manage_users'))


@app.route('/user/<int:id>/ban', methods=['POST'])
@admin_required
def toggle_user_ban(id):
    if id == session['user_id']:
        flash('Cannot ban your own account.')
        return redirect(url_for('manage_users'))


    try:
        user = db.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
        new_status = not user['is_banned']

        db.execute('''
            UPDATE users 
            SET is_banned = ?, updated_at = ?
            WHERE id = ?
        ''', (new_status, datetime.now(), id))
        db.commit()

        status = 'banned' if new_status else 'unbanned'
        flash(f'User {user["username"]} has been {status}.')

    except sqlite3.Error as e:
        db.rollback()
        flash(f'Error updating user status: {e}')

    return redirect(url_for('manage_users'))


@app.route('/users/export', methods=['POST'])
@admin_required
def export_users():

    users = db.execute('''
        SELECT u.id, u.username, u.email, u.role, u.created_at,
               COUNT(DISTINCT r.id) as recipe_count,
               COUNT(DISTINCT f.id) as favorite_count
        FROM users u
        LEFT JOIN recipes r ON u.id = r.user_id
        LEFT JOIN favorites f ON u.id = f.user_id
        GROUP BY u.id
    ''').fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Username', 'Email', 'Role', 'Created At',
                     'Recipe Count', 'Favorite Count'])

    for user in users:
        writer.writerow([
            user['id'],
            user['username'],
            user['email'],
            user['role'],
            user['created_at'],
            user['recipe_count'],
            user['favorite_count']
        ])

    output.seek(0)
    return send_from_directory(
        directory='.',
        path='users_export.csv',
        as_attachment=True,
        download_name=f'users_export_{datetime.now().strftime("%Y%m%d")}.csv',
        mimetype='text/csv'
    )


# Additional Recipe Management Routes
@app.route('/recipe/<int:id>/edit/ingredients', methods=['POST'])
@login_required
def edit_recipe_ingredients(id):

    recipe = db.execute(
        'SELECT * FROM recipes WHERE id = ? AND user_id = ?',
        (id, session['user_id'])
    ).fetchone()

    if recipe is None:
        abort(403)

    try:
        # Get ingredient data from request
        ingredients = request.json.get('ingredients', [])

        # Start transaction
        db.execute('BEGIN TRANSACTION')

        # Clear existing ingredients
        db.execute('DELETE FROM recipe_ingredients WHERE recipe_id = ?', (id,))

        # Add new ingredients
        for ingredient in ingredients:
            db.execute('''
                INSERT INTO recipe_ingredients 
                (recipe_id, name, amount, unit, notes, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id,
                  ingredient['name'],
                  ingredient['amount'],
                  ingredient.get('unit', ''),
                  ingredient.get('notes', ''),
                  ingredient.get('category', 'other')))

        # Update recipe's modified timestamp
        db.execute('''
            UPDATE recipes 
            SET updated_at = ?
            WHERE id = ?
        ''', (datetime.now(), id))

        db.execute('COMMIT')
        return jsonify({'success': True})

    except (sqlite3.Error, KeyError) as e:
        db.execute('ROLLBACK')
        return jsonify({'error': str(e)}), 400


@app.route('/recipe/<int:id>/edit/instructions', methods=['POST'])
@login_required
def edit_recipe_instructions(id):

    recipe = db.execute(
        'SELECT * FROM recipes WHERE id = ? AND user_id = ?',
        (id, session['user_id'])
    ).fetchone()

    if recipe is None:
        abort(403)

    try:
        instructions = request.json.get('instructions', [])

        db.execute('''
            UPDATE recipes 
            SET instructions = ?,
                updated_at = ?
            WHERE id = ?
        ''', (json.dumps(instructions), datetime.now(), id))

        db.commit()
        return jsonify({'success': True})

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400


@app.route('/recipe/<int:id>/edit/image', methods=['POST'])
@login_required
def edit_recipe_image(id):

    recipe = db.execute(
        'SELECT * FROM recipes WHERE id = ? AND user_id = ?',
        (id, session['user_id'])
    ).fetchone()

    if recipe is None:
        abort(403)

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']

    try:
        # Save new image
        image_filename = save_image(image)
        if not image_filename:
            return jsonify({'error': 'Invalid image file'}), 400

        # Delete old image
        if recipe['image']:
            delete_image(recipe['image'])

        # Update recipe
        db.execute('''
            UPDATE recipes 
            SET image = ?,
                updated_at = ?
            WHERE id = ?
        ''', (image_filename, datetime.now(), id))

        db.commit()
        return jsonify({
            'success': True,
            'image_url': url_for('static', filename=f'uploads/{image_filename}')
        })

    except Exception as e:
        if image_filename:
            delete_image(image_filename)
        return jsonify({'error': str(e)}), 400


@app.route('/recipe/<int:id>/edit/metadata', methods=['POST'])
@login_required
def edit_recipe_metadata(id):

    recipe = db.execute(
        'SELECT * FROM recipes WHERE id = ? AND user_id = ?',
        (id, session['user_id'])
    ).fetchone()

    if recipe is None:
        abort(403)

    try:
        data = request.json
        db.execute('''
            UPDATE recipes 
            SET name = ?,
                description = ?,
                category = ?,
                prep_time = ?,
                cook_time = ?,
                servings = ?,
                difficulty = ?,
                tags = ?,
                updated_at = ?
            WHERE id = ?
        ''', (
            data.get('name', recipe['name']),
            data.get('description', recipe['description']),
            data.get('category', recipe['category']),
            data.get('prep_time', recipe['prep_time']),
            data.get('cook_time', recipe['cook_time']),
            data.get('servings', recipe['servings']),
            data.get('difficulty', recipe['difficulty']),
            json.dumps(data.get('tags', [])),
            datetime.now(),
            id
        ))

        db.commit()
        return jsonify({'success': True})

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400


@app.route('/recipe/<int:id>/versions', methods=['GET'])
@login_required
def recipe_versions(id):

    versions = db.execute('''
        SELECT rv.*, u.username as editor
        FROM recipe_versions rv
        JOIN users u ON rv.user_id = u.id
        WHERE rv.recipe_id = ?
        ORDER BY rv.created_at DESC
    ''', (id,)).fetchall()

    return jsonify([dict(v) for v in versions])


@app.route('/recipe/<int:id>/restore/<int:version_id>', methods=['POST'])
@login_required
def restore_recipe_version(id, version_id):

    recipe = db.execute(
        'SELECT * FROM recipes WHERE id = ? AND user_id = ?',
        (id, session['user_id'])
    ).fetchone()

    if recipe is None:
        abort(403)

    try:
        # Get version data
        version = db.execute(
            'SELECT * FROM recipe_versions WHERE id = ? AND recipe_id = ?',
            (version_id, id)
        ).fetchone()

        if version is None:
            return jsonify({'error': 'Version not found'}), 404

        # Start transaction
        db.execute('BEGIN TRANSACTION')

        # Save current version
        db.execute('''
            INSERT INTO recipe_versions 
            (recipe_id, user_id, data, created_at)
            VALUES (?, ?, ?, ?)
        ''', (id, session['user_id'],
              json.dumps({
                  'name': recipe['name'],
                  'description': recipe['description'],
                  'instructions': recipe['instructions'],
                  'ingredients': [dict(i) for i in db.execute(
                      'SELECT * FROM recipe_ingredients WHERE recipe_id = ?',
                      (id,)).fetchall()]
              }),
              datetime.now()))

        # Restore version data
        version_data = json.loads(version['data'])

        # Update recipe
        db.execute('''
            UPDATE recipes 
            SET name = ?,
                description = ?,
                instructions = ?,
                updated_at = ?
            WHERE id = ?
        ''', (
            version_data['name'],
            version_data['description'],
            version_data['instructions'],
            datetime.now(),
            id
        ))

        # Restore ingredients
        db.execute('DELETE FROM recipe_ingredients WHERE recipe_id = ?', (id,))
        for ingredient in version_data['ingredients']:
            db.execute('''
                INSERT INTO recipe_ingredients 
                (recipe_id, name, amount, unit, notes, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id,
                  ingredient['name'],
                  ingredient['amount'],
                  ingredient.get('unit', ''),
                  ingredient.get('notes', ''),
                  ingredient.get('category', 'other')))

        db.execute('COMMIT')
        return jsonify({'success': True})

    except Exception as e:
        db.execute('ROLLBACK')
        return jsonify({'error': str(e)}), 400


# Recipe Search and Filtering
@app.route('/api/search/recipes', methods=['GET'])
@login_required
def search_recipes():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    time_range = request.args.get('time', '')
    tags = request.args.getlist('tags')


    sql_query = '''
        SELECT r.*, u.username as author,
               COUNT(DISTINCT f.id) as favorite_count,
               COUNT(DISTINCT c.id) as comment_count,
               EXISTS(SELECT 1 FROM favorites 
                     WHERE recipe_id = r.id 
                     AND user_id = ?) as is_favorite
        FROM recipes r
        JOIN users u ON r.user_id = u.id
        LEFT JOIN favorites f ON r.id = f.recipe_id
        LEFT JOIN comments c ON r.id = c.recipe_id
        WHERE 1=1
    '''
    params = [session['user_id']]

    if query:
        sql_query += ''' AND (
            r.name LIKE ? OR 
            r.description LIKE ? OR 
            r.instructions LIKE ? OR
            EXISTS(SELECT 1 FROM recipe_ingredients 
                  WHERE recipe_id = r.id AND name LIKE ?)
        )'''
        search_term = f'%{query}%'
        params.extend([search_term, search_term, search_term, search_term])

    if category:
        sql_query += ' AND r.category = ?'
        params.append(category)

    if difficulty:
        sql_query += ' AND r.difficulty = ?'
        params.append(difficulty)

    if time_range:
        if time_range == 'quick':
            sql_query += ' AND (r.prep_time + r.cook_time) <= 30'
        elif time_range == 'medium':
            sql_query += ' AND (r.prep_time + r.cook_time) BETWEEN 31 AND 60'
        elif time_range == 'long':
            sql_query += ' AND (r.prep_time + r.cook_time) > 60'

    if tags:
        placeholders = ','.join('?' * len(tags))
        sql_query += f''' AND EXISTS(
            SELECT 1 FROM recipe_tags 
            WHERE recipe_id = r.id AND tag IN ({placeholders})
        )'''
        params.extend(tags)

    sql_query += ' GROUP BY r.id ORDER BY r.created_at DESC'

    recipes = db.execute(sql_query, params).fetchall()
    return jsonify([dict(r) for r in recipes])


# Recipe Comments
@app.route('/api/recipe/<int:id>/comment', methods=['POST'])
@login_required
def api_add_comment(id):
    data = request.get_json()
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'success': False, 'message': 'Comment cannot be empty'})

    try:
        db.execute('''
            INSERT INTO comments (user_id, recipe_id, content, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (session['user_id'], id, content))
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': 'Failed to add comment'})

@app.route('/comment/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def manage_comment(id):

    comment = db.execute('''
        SELECT * FROM comments 
        WHERE id = ? AND user_id = ?
    ''', (id, session['user_id'])).fetchone()

    if comment is None:
        abort(403)

    if request.method == 'DELETE':
        db.execute('DELETE FROM comments WHERE id = ?', (id,))
        db.commit()
        return jsonify({'success': True})

    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Comment content is required'}), 400

    db.execute('''
        UPDATE comments 
        SET content = ?, updated_at = ?
        WHERE id = ?
    ''', (content, datetime.now(), id))
    db.commit()

    return jsonify({'success': True})


# Recipe Rating System
@app.route('/recipe/<int:id>/rate', methods=['POST'])
@login_required
def rate_recipe(id):
    rating = request.json.get('rating')
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'error': 'Invalid rating value'}), 400


    try:
        # Check if user already rated this recipe
        existing = db.execute('''
            SELECT * FROM recipe_ratings 
            WHERE recipe_id = ? AND user_id = ?
        ''', (id, session['user_id'])).fetchone()

        if existing:
            db.execute('''
                UPDATE recipe_ratings 
                SET rating = ?, updated_at = ?
                WHERE recipe_id = ? AND user_id = ?
            ''', (rating, datetime.now(), id, session['user_id']))
        else:
            db.execute('''
                INSERT INTO recipe_ratings 
                (recipe_id, user_id, rating, created_at)
                VALUES (?, ?, ?, ?)
            ''', (id, session['user_id'], rating, datetime.now()))

        db.commit()

        # Calculate new average rating
        avg_rating = db.execute('''
            SELECT AVG(rating) as avg_rating,
                   COUNT(*) as total_ratings
            FROM recipe_ratings
            WHERE recipe_id = ?
        ''', (id,)).fetchone()

        return jsonify({
            'success': True,
            'average_rating': float(avg_rating['avg_rating']),
            'total_ratings': avg_rating['total_ratings']
        })

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400


# Recipe Collections
@app.route('/collections', methods=['GET', 'POST'])
@login_required
def manage_collections():

    if request.method == 'POST':
        name = request.json.get('name')
        description = request.json.get('description', '')
        is_public = request.json.get('is_public', False)

        if not name:
            return jsonify({'error': 'Collection name is required'}), 400

        try:
            cursor = db.execute('''
                INSERT INTO recipe_collections 
                (name, description, is_public, user_id, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, description, is_public, session['user_id'], datetime.now()))

            collection_id = cursor.lastrowid
            db.commit()

            return jsonify({
                'success': True,
                'collection_id': collection_id
            })

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 400

    # Get user's collections with recipe counts
    collections = db.execute('''
        SELECT c.*, 
               COUNT(cr.recipe_id) as recipe_count
        FROM recipe_collections c
        LEFT JOIN collection_recipes cr ON c.id = cr.collection_id
        WHERE c.user_id = ?
        GROUP BY c.id
        ORDER BY c.name
    ''', (session['user_id'],)).fetchall()

    return jsonify([dict(c) for c in collections])


@app.route('/collection/<int:id>/recipes', methods=['POST', 'DELETE'])
@login_required
def manage_collection_recipes(id):
    recipe_id = request.json.get('recipe_id')
    if not recipe_id:
        return jsonify({'error': 'Recipe ID is required'}), 400


    collection = db.execute('''
        SELECT * FROM recipe_collections 
        WHERE id = ? AND user_id = ?
    ''', (id, session['user_id'])).fetchone()

    if collection is None:
        abort(403)

    try:
        if request.method == 'POST':
            db.execute('''
                INSERT INTO collection_recipes 
                (collection_id, recipe_id, added_at)
                VALUES (?, ?, ?)
            ''', (id, recipe_id, datetime.now()))
        else:
            db.execute('''
                DELETE FROM collection_recipes 
                WHERE collection_id = ? AND recipe_id = ?
            ''', (id, recipe_id))

        db.commit()
        return jsonify({'success': True})

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    helper = CategoryHelper()

    if request.method == 'POST':
        recipe = Recipe(
            title=request.form.get('title'),
            # ... other recipe fields ...
        )

        # Get ingredients data from form
        ingredients_data = zip(
            request.form.getlist('ingredients[]'),
            request.form.getlist('quantities[]'),
            request.form.getlist('units[]')
        )

        # Add ingredients to recipe
        for name, qty, unit in ingredients_data:
            ingredient = Ingredient(
                name=name,
                quantity=float(qty),
                unit=unit,
                category=helper.suggest_category(name)  # Get category suggestion
            )
            recipe.ingredients.append(ingredient)

        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('recipes'))

    return render_template('add_recipe.html',
                           available_ingredients=helper.get_available_ingredients(),
                           categories=helper.get_categories())


# Recipe Import/Export
@app.route('/api/recipes/import', methods=['POST'])
@login_required
def import_recipes():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.json'):
        return jsonify({'error': 'Only JSON files are supported'}), 400

    try:
        recipes_data = json.load(file)

        imported_count = 0
        errors = []

        db.execute('BEGIN TRANSACTION')

        for recipe_data in recipes_data:
            try:
                # Insert recipe
                cursor = db.execute('''
                    INSERT INTO recipes (
                        name, description, instructions, category,
                        prep_time, cook_time, servings, difficulty,
                        user_id, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    recipe_data['name'],
                    recipe_data.get('description', ''),
                    recipe_data['instructions'],
                    recipe_data.get('category', 'other'),
                    recipe_data.get('prep_time', 0),
                    recipe_data.get('cook_time', 0),
                    recipe_data.get('servings', 1),
                    recipe_data.get('difficulty', 'medium'),
                    session['user_id'],
                    datetime.now()
                ))
                recipe_id = cursor.lastrowid

                # Insert ingredients
                for ingredient in recipe_data.get('ingredients', []):
                    db.execute('''
                        INSERT INTO recipe_ingredients (
                            recipe_id, name, amount, unit, category
                        ) VALUES (?, ?, ?, ?, ?)
                    ''', (
                        recipe_id,
                        ingredient['name'],
                        ingredient.get('amount', ''),
                        ingredient.get('unit', ''),
                        ingredient.get('category', 'other')
                    ))

                # Insert tags
                for tag in recipe_data.get('tags', []):
                    db.execute('''
                        INSERT INTO recipe_tags (recipe_id, tag)
                        VALUES (?, ?)
                    ''', (recipe_id, tag))

                imported_count += 1

            except KeyError as e:
                errors.append(f"Missing required field in recipe: {str(e)}")
            except sqlite3.Error as e:
                errors.append(f"Database error: {str(e)}")

        if imported_count > 0:
            db.execute('COMMIT')
            return jsonify({
                'success': True,
                'imported_count': imported_count,
                'errors': errors
            })
        else:
            db.execute('ROLLBACK')
            return jsonify({
                'error': 'No recipes were imported',
                'details': errors
            }), 400

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/recipes/export', methods=['POST'])
@login_required
def export_recipes():
    recipe_ids = request.json.get('recipe_ids', [])
    export_format = request.json.get('format', 'json')



    if export_format == 'json':
        recipes = []
        for recipe_id in recipe_ids:
            recipe = db.execute('''
                SELECT r.*, u.username as author
                FROM recipes r
                JOIN users u ON r.user_id = u.id
                WHERE r.id = ?
            ''', (recipe_id,)).fetchone()

            if recipe:
                recipe_dict = dict(recipe)

                # Get ingredients
                ingredients = db.execute('''
                    SELECT name, amount, unit, category
                    FROM recipe_ingredients
                    WHERE recipe_id = ?
                ''', (recipe_id,)).fetchall()
                recipe_dict['ingredients'] = [dict(i) for i in ingredients]

                # Get tags
                tags = db.execute('''
                    SELECT tag FROM recipe_tags
                    WHERE recipe_id = ?
                ''', (recipe_id,)).fetchall()
                recipe_dict['tags'] = [t['tag'] for t in tags]

                # Get ratings
                ratings = db.execute('''
                    SELECT AVG(rating) as avg_rating,
                           COUNT(*) as total_ratings
                    FROM recipe_ratings
                    WHERE recipe_id = ?
                ''', (recipe_id,)).fetchone()
                recipe_dict['rating'] = {
                    'average': float(ratings['avg_rating']) if ratings['avg_rating'] else 0,
                    'count': ratings['total_ratings']
                }

                recipes.append(recipe_dict)

        return jsonify(recipes)

    elif export_format == 'pdf':
        # PDF export implementation
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            for recipe_id in recipe_ids:
                recipe = db.execute('''
                    SELECT r.*, u.username as author
                    FROM recipes r
                    JOIN users u ON r.user_id = u.id
                    WHERE r.id = ?
                ''', (recipe_id,)).fetchone()

                if recipe:
                    # Add recipe title
                    story.append(Paragraph(recipe['name'], styles['Heading1']))
                    story.append(Spacer(1, 12))

                    # Add description
                    if recipe['description']:
                        story.append(Paragraph(recipe['description'], styles['Normal']))
                        story.append(Spacer(1, 12))

                    # Add ingredients
                    story.append(Paragraph('Ingredients:', styles['Heading2']))
                    ingredients = db.execute('''
                        SELECT * FROM recipe_ingredients
                        WHERE recipe_id = ?
                        ORDER BY category, name
                    ''', (recipe_id,)).fetchall()

                    for ingredient in ingredients:
                        text = f"• {ingredient['amount']} {ingredient['unit']} {ingredient['name']}"
                        story.append(Paragraph(text, styles['Normal']))

                    story.append(Spacer(1, 12))

                    # Add instructions
                    story.append(Paragraph('Instructions:', styles['Heading2']))
                    instructions = recipe['instructions'].split('\n')
                    for i, step in enumerate(instructions, 1):
                        if step.strip():
                            story.append(Paragraph(f"{i}. {step}", styles['Normal']))

                    story.append(Spacer(1, 20))

            doc.build(story)
            buffer.seek(0)

            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'recipes_{datetime.now().strftime("%Y%m%d")}.pdf',
                mimetype='application/pdf'
            )

        except Exception as e:
            return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

    else:
        return jsonify({'error': 'Unsupported export format'}), 400


# Recipe Nutrition Information
@app.route('/api/recipe/<int:id>/nutrition', methods=['GET', 'POST'])
@login_required
def recipe_nutrition(id):

    recipe = db.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()

    if recipe is None:
        abort(404)

    if request.method == 'POST':
        if session['user_id'] != recipe['user_id']:
            abort(403)

        nutrition_data = request.json
        try:
            db.execute('''
                INSERT OR REPLACE INTO recipe_nutrition (
                    recipe_id, calories, protein, carbohydrates,
                    fat, fiber, sugar, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                id,
                nutrition_data.get('calories', 0),
                nutrition_data.get('protein', 0),
                nutrition_data.get('carbohydrates', 0),
                nutrition_data.get('fat', 0),
                nutrition_data.get('fiber', 0),
                nutrition_data.get('sugar', 0),
                datetime.now()
            ))
            db.commit()
            return jsonify({'success': True})

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 400

    # GET request - retrieve nutrition info
    nutrition = db.execute('''
        SELECT * FROM recipe_nutrition
        WHERE recipe_id = ?
    ''', (id,)).fetchone()

    return jsonify(dict(nutrition) if nutrition else {})


# Recipe Sharing
@app.route('/api/recipe/<int:id>/share', methods=['POST'])
@login_required
def share_recipe(id):
    share_type = request.json.get('type')
    recipient = request.json.get('recipient')


    recipe = db.execute('''
        SELECT r.*, u.username as author
        FROM recipes r
        JOIN users u ON r.user_id = u.id
        WHERE r.id = ?
    ''', (id,)).fetchone()

    if recipe is None:
        abort(404)

    if share_type == 'email':
        try:
            # Email sharing implementation
            pass
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif share_type == 'internal':
        try:
            recipient_user = get_user_by_username(recipient)
            if recipient_user is None:
                return jsonify({'error': 'Recipient not found'}), 404

            db.execute('''
                INSERT INTO shared_recipes (
                    recipe_id, shared_by, shared_with, created_at
                ) VALUES (?, ?, ?, ?)
            ''', (id, session['user_id'], recipient_user['id'], datetime.now()))
            db.commit()

            return jsonify({'success': True})

        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 400

    else:
        return jsonify({'error': 'Invalid share type'}), 400


# Advanced Analytics and Statistics
@app.route('/api/analytics/user/<int:user_id>')
@admin_required
def user_analytics(user_id):

    try:
        # User activity metrics
        metrics = db.execute('''
            SELECT 
                COUNT(DISTINCT r.id) as total_recipes,
                COUNT(DISTINCT f.id) as total_favorites,
                COUNT(DISTINCT c.id) as total_comments,
                COUNT(DISTINCT rr.id) as total_ratings,
                AVG(rr.rating) as avg_rating_given,
                (SELECT AVG(rating) 
                 FROM recipe_ratings 
                 WHERE recipe_id IN (SELECT id FROM recipes WHERE user_id = ?)) as avg_rating_received,
                (SELECT COUNT(DISTINCT user_id) 
                 FROM favorites 
                 WHERE recipe_id IN (SELECT id FROM recipes WHERE user_id = ?)) as total_followers
            FROM users u
            LEFT JOIN recipes r ON u.id = r.user_id
            LEFT JOIN favorites f ON u.id = f.user_id
            LEFT JOIN comments c ON u.id = c.user_id
            LEFT JOIN recipe_ratings rr ON u.id = rr.user_id
            WHERE u.id = ?
            GROUP BY u.id
        ''', (user_id, user_id, user_id)).fetchone()

        # Activity timeline
        timeline = db.execute('''
            SELECT 
                date(created_at) as date,
                COUNT(CASE WHEN type = 'recipe' THEN 1 END) as recipes_created,
                COUNT(CASE WHEN type = 'favorite' THEN 1 END) as recipes_favorited,
                COUNT(CASE WHEN type = 'comment' THEN 1 END) as comments_made,
                COUNT(CASE WHEN type = 'rating' THEN 1 END) as ratings_given
            FROM (
                SELECT id, 'recipe' as type, created_at FROM recipes WHERE user_id = ?
                UNION ALL
                SELECT id, 'favorite' as type, created_at FROM favorites WHERE user_id = ?
                UNION ALL
                SELECT id, 'comment' as type, created_at FROM comments WHERE user_id = ?
                UNION ALL
                SELECT id, 'rating' as type, created_at FROM recipe_ratings WHERE user_id = ?
            )
            GROUP BY date(created_at)
            ORDER BY date DESC
            LIMIT 30
        ''', (user_id, user_id, user_id, user_id)).fetchall()

        # Popular recipes
        popular_recipes = db.execute('''
            SELECT 
                r.*,
                COUNT(DISTINCT f.id) as favorite_count,
                COUNT(DISTINCT c.id) as comment_count,
                AVG(rr.rating) as avg_rating,
                COUNT(DISTINCT rr.id) as rating_count
            FROM recipes r
            LEFT JOIN favorites f ON r.id = f.recipe_id
            LEFT JOIN comments c ON r.id = c.recipe_id
            LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
            WHERE r.user_id = ?
            GROUP BY r.id
            ORDER BY (
                COUNT(DISTINCT f.id) * 2 + 
                COUNT(DISTINCT c.id) + 
                COALESCE(AVG(rr.rating), 0)
            ) DESC
            LIMIT 5
        ''', (user_id,)).fetchall()

        return jsonify({
            'metrics': dict(metrics),
            'timeline': [dict(t) for t in timeline],
            'popular_recipes': [dict(r) for r in popular_recipes]
        })

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500


# Recipe Recommendations
@app.route('/api/recommendations')
@login_required
def get_recommendations():

    try:
        # Based on user's favorites
        favorite_based = db.execute('''
            SELECT r.*, 
                   COUNT(DISTINCT f2.user_id) as similar_users,
                   COUNT(DISTINCT c.id) as comment_count,
                   AVG(rr.rating) as avg_rating
            FROM recipes r
            JOIN favorites f1 ON f1.recipe_id IN (
                SELECT recipe_id 
                FROM favorites 
                WHERE user_id = ?
            )
            JOIN favorites f2 ON f2.user_id = f1.user_id
            LEFT JOIN comments c ON r.id = c.recipe_id
            LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
            WHERE r.id NOT IN (
                SELECT recipe_id 
                FROM favorites 
                WHERE user_id = ?
            )
            GROUP BY r.id
            ORDER BY similar_users DESC
            LIMIT 5
        ''', (session['user_id'], session['user_id'])).fetchall()

        # Based on recently viewed
        recently_viewed = db.execute('''
            SELECT r.*, 
                   COUNT(DISTINCT f.id) as favorite_count,
                   COUNT(DISTINCT c.id) as comment_count,
                   AVG(rr.rating) as avg_rating
            FROM recipes r
            JOIN recipe_views rv ON r.id = rv.recipe_id
            LEFT JOIN favorites f ON r.id = f.recipe_id
            LEFT JOIN comments c ON r.id = c.recipe_id
            LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
            WHERE rv.user_id = ?
            GROUP BY r.id
            ORDER BY rv.viewed_at DESC
            LIMIT 5
        ''', (session['user_id'],)).fetchall()

        # Based on user's cooking history
        cooking_history_based = db.execute('''
            SELECT r.*, 
                   COUNT(DISTINCT f.id) as favorite_count,
                   COUNT(DISTINCT c.id) as comment_count,
                   AVG(rr.rating) as avg_rating
            FROM recipes r
            JOIN recipe_ingredients ri1 ON r.id = ri1.recipe_id
            JOIN recipe_ingredients ri2 ON ri1.name = ri2.name
            JOIN cooking_history ch ON ri2.recipe_id = ch.recipe_id
            LEFT JOIN favorites f ON r.id = f.recipe_id
            LEFT JOIN comments c ON r.id = c.recipe_id
            LEFT JOIN recipe_ratings rr ON r.id = rr.recipe_id
            WHERE ch.user_id = ?
            AND r.id NOT IN (SELECT recipe_id FROM cooking_history WHERE user_id = ?)
            GROUP BY r.id
            ORDER BY COUNT(DISTINCT ri1.id) DESC
            LIMIT 5
        ''', (session['user_id'], session['user_id'])).fetchall()

        return jsonify({
            'favorite_based': [dict(r) for r in favorite_based],
            'recently_viewed': [dict(r) for r in recently_viewed],
            'cooking_history_based': [dict(r) for r in cooking_history_based]
        })

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500


# System Maintenance and Cleanup
@app.cli.command('cleanup')
def cleanup_command():
    """Remove unused images and clean up the database."""

    try:
        # Find unused images
        used_images = set()
        for table in ['recipes', 'users']:
            images = db.execute(f'SELECT image FROM {table} WHERE image IS NOT NULL').fetchall()
            used_images.update(img['image'] for img in images)

        # Check upload directory
        upload_dir = app.config['UPLOAD_FOLDER']
        removed = 0
        for filename in os.listdir(upload_dir):
            if filename not in used_images:
                os.remove(os.path.join(upload_dir, filename))
                removed += 1

        # Clean up old sessions
        db.execute('DELETE FROM sessions WHERE expires < ?', (datetime.now(),))

        # Remove orphaned records
        db.execute('DELETE FROM recipe_ingredients WHERE recipe_id NOT IN (SELECT id FROM recipes)')
        db.execute('DELETE FROM recipe_tags WHERE recipe_id NOT IN (SELECT id FROM recipes)')
        db.execute('DELETE FROM favorites WHERE recipe_id NOT IN (SELECT id FROM recipes)')
        db.execute('DELETE FROM comments WHERE recipe_id NOT IN (SELECT id FROM recipes)')
        db.execute('DELETE FROM recipe_ratings WHERE recipe_id NOT IN (SELECT id FROM recipes)')

        db.commit()
        click.echo(f'Cleanup completed: Removed {removed} unused images')

    except (sqlite3.Error, OSError) as e:
        db.rollback()
        click.echo(f'Error during cleanup: {e}')


# Background Tasks
def update_search_index():
    """Update the search index for recipes."""

    try:
        db.execute('BEGIN TRANSACTION')

        # Clear existing index
        db.execute('DELETE FROM recipe_search_index')

        # Index all recipes
        recipes = db.execute('''
            SELECT r.id, r.name, r.description, r.instructions,
                   GROUP_CONCAT(ri.name) as ingredients,
                   GROUP_CONCAT(rt.tag) as tags
            FROM recipes r
            LEFT JOIN recipe_ingredients ri ON r.id = ri.recipe_id
            LEFT JOIN recipe_tags rt ON r.id = rt.recipe_id
            GROUP BY r.id
        ''').fetchall()

        for recipe in recipes:
            search_text = ' '.join(filter(None, [
                recipe['name'],
                recipe['description'],
                recipe['instructions'],
                recipe['ingredients'],
                recipe['tags']
            ]))

            db.execute('''
                INSERT INTO recipe_search_index (recipe_id, search_text)
                VALUES (?, ?)
            ''', (recipe['id'], search_text))

        db.execute('COMMIT')

    except sqlite3.Error as e:
        db.execute('ROLLBACK')
        app.logger.error(f'Error updating search index: {e}')


"""if __name__ == '__main__':
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ensure upload folder exists
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    app.run(debug=True)
"""


# the corrected background task code
def run_schedule():
    """Run scheduled tasks in a background thread."""
    while True:
        try:
            # Run maintenance tasks
            with app.app_context():  # Using app is correct
                update_search_index()
                # Add other periodic tasks here

            # Sleep for 24 hours
            time.sleep(24 * 60 * 60)

        except Exception as e:
            app.logger.error(f'Error in scheduled task: {e}')  # Using app is correct
            # Sleep for 1 hour on error
            time.sleep(60 * 60)


# Add this route for handling message transfers after login
@app.route('/transfer-to-messages', methods=['GET', 'POST'])
@login_required
def transfer_to_messages():
    if request.method == 'POST':
        try:
            # Get user info
            user_id = session.get('user_id')
            if not user_id:
                flash('Please login first')
                return redirect(url_for('login'))

            # Get message data if any
            message = request.form.get('message', '')
            recipient_id = request.form.get('recipient_id')

            # Redirect to messages page
            return redirect(url_for('messages'))

        except Exception as e:
            app.logger.error(f"Transfer error: {str(e)}")
            flash('Error during transfer')
            return redirect(url_for('login'))

    # GET request - show transfer page
    return render_template('transfer.html')


# Add the messages route
@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html')


@app.route('/recipes')
@login_required
def recipes():
    search = request.args.get('search', '')
    category = request.args.get('category', '')

    # Start with base query
    query = db.session.query(
        Recipe,
        User.username.label('author'),
        db.func.count(db.distinct(Favorite.id)).label('favorite_count'),
        db.func.count(db.distinct(Comment.id)).label('comment_count')
    ).select_from(Recipe) \
     .join(User, User.id == Recipe.user_id) \
     .outerjoin(Favorite, Favorite.recipe_id == Recipe.id) \
     .outerjoin(Comment, Comment.recipe_id == Recipe.id)

    # Add filters
    if search:
        query = query.filter(
            db.or_(
                Recipe.name.ilike(f'%{search}%'),
                Recipe.description.ilike(f'%{search}%')
            )
        )

    if category:
        query = query.filter(Recipe.category == category)

    # Group and order
    recipes_data = query \
        .group_by(Recipe.id, User.username) \
        .order_by(Recipe.created_at.desc()) \
        .all()

    # Transform the results
    recipes = [{
        'id': row.Recipe.id,
        'name': row.Recipe.name,
        'description': row.Recipe.description,
        'image': row.Recipe.image,
        'author': row.author,
        'favorite_count': row.favorite_count,
        'comment_count': row.comment_count
    } for row in recipes_data]

    return render_template(
        'recipes.html',
        recipes=recipes,
        search=search,
        category=category
    )

# API endpoint if needed
@app.route('/recipes')
@login_required
def list_recipes():
    search = request.args.get('search', '')
    category = request.args.get('category', '')

    # Start with base query with explicit join conditions
    query = Recipe.query \
        .join(User, Recipe.user_id == User.id) \
        .outerjoin(Favorite, Recipe.id == Favorite.recipe_id) \
        .outerjoin(Comment, Recipe.id == Comment.recipe_id) \
        .with_entities(
            Recipe,
            User.username.label('author'),
            db.func.count(db.distinct(Favorite.id)).label('favorite_count'),
            db.func.count(db.distinct(Comment.id)).label('comment_count')
        )

    # Add filters
    if search:
        query = query.filter(
            db.or_(
                Recipe.name.ilike(f'%{search}%'),
                Recipe.description.ilike(f'%{search}%')
            )
        )

    if category:
        query = query.filter(Recipe.category == category)

    # Group and order
    recipes = query \
        .group_by(Recipe.id, User.username) \
        .order_by(Recipe.created_at.desc()) \
        .all()

    return render_template(
        'recipes.html',
        recipes=recipes,
        search=search,
        category=category
    )

# Start background thread if not in debug mode
if not app.debug:  # Using app is correct
    scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
    scheduler_thread.start()

# Main entry point
if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize database
    with app.app_context():
        db.create_all()

    # Run the app
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=True
    )
