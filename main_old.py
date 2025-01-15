import sqlite3
from datetime import datetime
from functools import wraps

"""from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime"""

from flask import Flask
from flask import render_template, redirect, url_for, request, flash
from flask import session, g, jsonify, send_from_directory
from flask_login import LoginManager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dev'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User1(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    category = db.Column(db.String(50))
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))
    category = db.Column(db.String(50))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)


class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    return redirect(url_for('login'))


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'instance/recipes.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'

        if error is None:
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)  # Store plain password
            )
            db.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("\n=== Login Debug ===")
        print("Request form:", request.form)
        print("Request JSON:", request.get_json())
        print("Request data:", request.data)
        print("===================\n")

        # Try both form data and JSON
        form_data = request.form
        json_data = request.get_json()

        username = form_data.get('username') if form_data else json_data.get('username') if json_data else None
        password = form_data.get('password') if form_data else json_data.get('password') if json_data else None

        print(f"Processed - Username: {username}, Password: {password}")

        db = get_db()

        try:
            user = db.execute(
                'SELECT * FROM users WHERE username = ?', (username,)
            ).fetchone()
            print(f"Found user in DB:", dict(user) if user else None)

            if user is None:
                return jsonify({'error': 'Incorrect username.'}), 401
            elif user['password'] != password:
                return jsonify({'error': 'Incorrect password.'}), 401

            session.clear()
            session['user_id'] = user['id']
            return jsonify({'success': True, 'redirect': url_for('dashboard')})

        except Exception as e:
            print(f"Login error: {e}")
            return jsonify({'error': str(e)}), 500

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE id = ?', (session['user_id'],)
    ).fetchone()

    return render_template('profile.html', user=user)


@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        description = data.get('description')
        prep_time = data.get('prep_time')
        servings = data.get('servings')
        instructions = data.get('instructions')
        ingredients = data.get('ingredients', [])

        if not name or not category:
            return jsonify({'error': 'Name and category are required'}), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO recipes (user_id, name, category, description, prep_time, servings, instructions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session['user_id'], name, category, description, prep_time, servings, instructions))

        recipe_id = cursor.lastrowid

        for ingredient in ingredients:
            cursor.execute("""
                INSERT INTO ingredients (recipe_id, name, amount, unit, description, category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (recipe_id, ingredient['name'], ingredient['amount'],
                  ingredient['unit'], ingredient.get('description'), ingredient.get('category')))

        db.commit()
        return jsonify({'id': recipe_id, 'message': 'Recipe created'})

    else:  # GET request
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT r.id, r.name, r.category, r.description, r.prep_time, r.servings, r.instructions
            FROM recipes r
            ORDER BY r.name
        """)

        recipes = []
        for row in cursor.fetchall():
            recipe = {
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'description': row[3],
                'prep_time': row[4],
                'servings': row[5],
                'instructions': row[6]
            }

            cursor.execute("""
                SELECT name, amount, unit, description, category
                FROM ingredients
                WHERE recipe_id = ?
            """, (recipe['id'],))

            recipe['ingredients'] = [{
                'name': ing[0],
                'amount': ing[1],
                'unit': ing[2],
                'description': ing[3],
                'category': ing[4]
            } for ing in cursor.fetchall()]

            recipes.append(recipe)

        return jsonify(recipes)


@app.route('/recipe/<int:recipe_id>', methods=['GET', 'PUT', 'DELETE'])
def recipe(recipe_id):
    if request.method in ['PUT', 'DELETE'] and 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    db = get_db()
    cursor = db.cursor()

    if request.method == 'PUT':
        data = request.get_json()

        cursor.execute("""
            UPDATE recipes
            SET name = ?, category = ?, description = ?, 
                prep_time = ?, servings = ?, instructions = ?
            WHERE id = ? AND user_id = ?
        """, (data['name'], data['category'], data.get('description'),
              data.get('prep_time'), data.get('servings'), data.get('instructions'),
              recipe_id, session['user_id']))

        if 'ingredients' in data:
            cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))

            for ingredient in data['ingredients']:
                cursor.execute("""
                    INSERT INTO ingredients (recipe_id, name, amount, unit, description, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (recipe_id, ingredient['name'], ingredient['amount'],
                      ingredient['unit'], ingredient.get('description'), ingredient.get('category')))

        db.commit()
        return jsonify({'message': 'Recipe updated'})

    elif request.method == 'DELETE':
        cursor.execute("""
            DELETE FROM recipes
            WHERE id = ? AND user_id = ?
        """, (recipe_id, session['user_id']))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Recipe not found or not authorized'}), 404

        db.commit()
        return jsonify({'message': 'Recipe deleted'})

    else:  # GET request
        cursor.execute("""
            SELECT r.id, r.name, r.category, r.description, r.prep_time, r.servings, r.instructions
            FROM recipes r
            WHERE r.id = ?
        """, (recipe_id,))

        recipe = cursor.fetchone()

        if recipe is None:
            return jsonify({'error': 'Recipe not found'}), 404

        cursor.execute("""
            SELECT name, amount, unit, description, category
            FROM ingredients
            WHERE recipe_id = ?
        """, (recipe_id,))

        ingredients = cursor.fetchall()

        return jsonify({
            'id': recipe[0],
            'name': recipe[1],
            'category': recipe[2],
            'description': recipe[3],
            'prep_time': recipe[4],
            'servings': recipe[5],
            'instructions': recipe[6],
            'ingredients': [{
                'name': ing[0],
                'amount': ing[1],
                'unit': ing[2],
                'description': ing[3],
                'category': ing[4]
            } for ing in ingredients]
        })


@app.route('/shopping-list', methods=['GET', 'POST'])
def shopping_list():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    if request.method == 'POST':
        db = get_db()
        data = request.get_json()

        recipe_id = data.get('recipe_id')

        if not recipe_id:
            return jsonify({'error': 'Missing recipe_id'}), 400

        cursor = db.cursor()

        cursor.execute("""
            SELECT id, name, amount, unit
            FROM ingredients
            WHERE recipe_id = ?
        """, (recipe_id,))

        ingredients = cursor.fetchall()

        for ing in ingredients:
            cursor.execute("""
                INSERT INTO shopping_list (user_id, recipe_id, ingredient_id, amount)
                VALUES (?, ?, ?, ?)
            """, (session['user_id'], recipe_id, ing[0], ing[2]))

        db.commit()
        return jsonify({'message': 'Added to shopping list'})

    else:  # GET request
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT sl.id, r.name as recipe_name, i.name as ingredient_name, 
                   sl.amount, i.unit, sl.checked
            FROM shopping_list sl
            JOIN recipes r ON sl.recipe_id = r.id
            JOIN ingredients i ON sl.ingredient_id = i.id
            WHERE sl.user_id = ?
            ORDER BY r.name, i.name
        """, (session['user_id'],))

        items = [{
            'id': row[0],
            'recipe_name': row[1],
            'ingredient_name': row[2],
            'amount': row[3],
            'unit': row[4],
            'checked': bool(row[5])
        } for row in cursor.fetchall()]

        return jsonify(items)


@app.route('/shopping-list/check/<int:item_id>', methods=['POST'])
def check_shopping_item(item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    db = get_db()
    cursor = db.cursor()

    data = request.get_json()
    checked = data.get('checked', False)

    cursor.execute("""
        UPDATE shopping_list
        SET checked = ?
        WHERE id = ? AND user_id = ?
    """, (checked, item_id, session['user_id']))

    db.commit()
    return jsonify({'message': 'Updated'})


@app.route('/shopping-list/clear', methods=['POST'])
def clear_shopping_list():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM shopping_list
        WHERE user_id = ? AND checked = 1
    """, (session['user_id'],))

    db.commit()
    return jsonify({'message': 'Cleared checked items'})


@app.route('/favorites', methods=['GET', 'POST', 'DELETE'])
def favorites():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json()
        recipe_id = data.get('recipe_id')

        if not recipe_id:
            return jsonify({'error': 'Missing recipe_id'}), 400

        try:
            cursor.execute("""
                INSERT INTO favorites (user_id, recipe_id)
                VALUES (?, ?)
            """, (session['user_id'], recipe_id))
            db.commit()
            return jsonify({'message': 'Added to favorites'})
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Already in favorites'}), 400

    elif request.method == 'DELETE':
        data = request.get_json()
        recipe_id = data.get('recipe_id')

        if not recipe_id:
            return jsonify({'error': 'Missing recipe_id'}), 400

        cursor.execute("""
            DELETE FROM favorites
            WHERE user_id = ? AND recipe_id = ?
        """, (session['user_id'], recipe_id))

        db.commit()
        return jsonify({'message': 'Removed from favorites'})

    else:  # GET request
        cursor.execute("""
            SELECT r.id, r.name, r.category, r.description
            FROM favorites f
            JOIN recipes r ON f.recipe_id = r.id
            WHERE f.user_id = ?
            ORDER BY r.name
        """, (session['user_id'],))

        favorites = [{
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'description': row[3]
        } for row in cursor.fetchall()]

        return jsonify(favorites)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')

    db = get_db()
    cursor = db.cursor()

    sql = """
        SELECT r.id, r.name, r.category, r.description, r.image_path
        FROM recipes r
        WHERE 1=1
    """
    params = []

    if query:
        sql += " AND (r.name LIKE ? OR r.description LIKE ?)"
        params.extend([f'%{query}%', f'%{query}%'])

    if category:
        sql += " AND r.category = ?"
        params.append(category)

    cursor.execute(sql + " ORDER BY r.name", params)

    recipes = [{
        'id': row[0],
        'name': row[1],
        'category': row[2],
        'description': row[3],
        'image': row[4] if row[4] else '/static/images/default-recipe.jpg'
    } for row in cursor.fetchall()]

    return jsonify(recipes)


@app.route('/categories')
def get_categories():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT DISTINCT category
        FROM recipes
        ORDER BY category
    """)

    categories = [row[0] for row in cursor.fetchall()]
    return jsonify(categories)


@app.route('/user/recipes')
@login_required
def user_recipes():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name, category, description
        FROM recipes
        WHERE user_id = ?
        ORDER BY name
    """, (session['user_id'],))

    recipes = [{
        'id': row[0],
        'name': row[1],
        'category': row[2],
        'description': row[3]
    } for row in cursor.fetchall()]

    return jsonify(recipes)


@app.route('/user/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    if request.method == 'POST':
        data = request.get_json()
        new_password = data.get('password')

        if new_password:
            db = get_db()
            db.execute(
                'UPDATE users SET password = ? WHERE id = ?',
                (new_password, session['user_id'])
            )
            db.commit()
            return jsonify({'message': 'Settings updated'})

    return jsonify({'error': 'Invalid request'}), 400


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    import traceback
    print(f"500 Error: {error}")
    print(traceback.format_exc())
    return jsonify({
        'error': 'Internal server error',
        'details': str(error),
        'trace': traceback.format_exc()
    }), 500


@app.route('/api/recipes', methods=['GET'])
def api_recipes():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT r.id, r.name, r.category, r.description, r.prep_time, r.servings, r.instructions
        FROM recipes r
        ORDER BY r.name
    """)

    recipes = []
    for row in cursor.fetchall():
        recipe = {
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'description': row[3],
            'prep_time': row[4],
            'servings': row[5],
            'instructions': row[6]
        }

        cursor.execute("""
            SELECT name, amount, unit, description, category
            FROM ingredients
            WHERE recipe_id = ?
        """, (recipe['id'],))

        recipe['ingredients'] = [{
            'name': ing[0],
            'amount': ing[1],
            'unit': ing[2],
            'description': ing[3],
            'category': ing[4]
        } for ing in cursor.fetchall()]

        recipes.append(recipe)

    return jsonify(recipes)


@app.route('/api/recipe/<int:recipe_id>')
def api_recipe(recipe_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT r.id, r.name, r.category, r.description, r.prep_time, r.servings, r.instructions
        FROM recipes r
        WHERE r.id = ?
    """, (recipe_id,))

    recipe = cursor.fetchone()

    if recipe is None:
        return jsonify({'error': 'Recipe not found'}), 404

    cursor.execute("""
        SELECT name, amount, unit, description, category
        FROM ingredients
        WHERE recipe_id = ?
    """, (recipe_id,))

    ingredients = cursor.fetchall()

    return jsonify({
        'id': recipe[0],
        'name': recipe[1],
        'category': recipe[2],
        'description': recipe[3],
        'prep_time': recipe[4],
        'servings': recipe[5],
        'instructions': recipe[6],
        'ingredients': [{
            'name': ing[0],
            'amount': ing[1],
            'unit': ing[2],
            'description': ing[3],
            'category': ing[4]
        } for ing in ingredients]
    })


@app.route('/api/recipe/<int:recipe_id>/details')
def get_recipe_details(recipe_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT r.id, r.name, r.category, r.description, r.instructions, r.prep_time, r.servings
        FROM recipes r WHERE r.id = ?
    ''', (recipe_id,))
    recipe = cursor.fetchone()
    if recipe is None:
        return jsonify({'error': 'Recipe not found'}), 404

    cursor.execute('SELECT name, amount, unit FROM ingredients WHERE recipe_id = ?', (recipe_id,))
    ingredients = [{'name': row[0], 'amount': row[1], 'unit': row[2]} for row in cursor.fetchall()]

    return jsonify({
        'id': recipe[0],
        'name': recipe[1],
        'category': recipe[2],
        'description': recipe[3],
        'instructions': recipe[4],
        'prep_time': recipe[5],
        'servings': recipe[6],
        'ingredients': ingredients
    })


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/recipe/view/<int:recipe_id>')
def view_recipe(recipe_id):
    return render_template('recipe_details.html', recipe_id=recipe_id)


@app.route('/recipe/details/<int:recipe_id>')
def recipe_details(recipe_id):
    return render_template('recipe_details.html', recipe_id=recipe_id)


@app.route('/api/users')
def get_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, username FROM users')
    users = [{'id': row[0], 'username': row[1]} for row in cursor.fetchall()]
    return jsonify(users)


@app.route('/api/shopping-list')
def get_shopping_list():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, amount, unit, checked FROM shopping_list')
    items = [{'id': row[0], 'name': row[1], 'amount': row[2], 'unit': row[3], 'checked': row[4]}
             for row in cursor.fetchall()]
    return jsonify(items)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
