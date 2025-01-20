import os
import sys
from flask import Flask
from extensions import db, login_manager
from flask_migrate import Migrate
from app_config import config
import models
from extensions import db, login_manager
from sqlalchemy import text
from app import create_app
from config import Config
from jinja2 import Environment
from flask_login import LoginManager
from routes.auth import auth_bp

sys.path.append(os.path.dirname(os.path.abspath(__file__)))




@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


def nl2br(value):
    return value.replace('\n', '<br>\n')


def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    # Get absolute path for database
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'recipes.db')

    # Load config
    app.config.from_object(Config)

    # Override database URI with absolute path
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set configuration
    app.config.update(config)


    # Initialize extensions
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    db.init_app(app)
    login_manager.init_app(app)

    # Setup login manager
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        if user_id is None:
            return None
        return models.User.query.get(int(user_id))

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register blueprints

    from routes.recipe import recipe_bp




    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialize extensions

    login_manager.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Import blueprints
    from routes.admin import admin_bp
    from routes.auth import auth_bp
    from routes.main import main_bp

    from routes.shopping import shopping_bp
    from routes.collaborative import collaborative_bp
    from routes.ingredient import ingredient_bp
    from routes.category import category_bp
    from routes.favorite import favorite_bp
    from routes.comment import comment_bp
    from routes.template import template_bp

    # Register blueprints in order of specificity
    app.register_blueprint(recipe_bp, url_prefix='/recipe')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(shopping_bp)
    app.register_blueprint(collaborative_bp)
    app.register_blueprint(ingredient_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(template_bp)

    def nl2br(value):
        return value.replace('\n', '<br>\n')

    # Register jinja2 filters
    app.jinja_env.filters['nl2br'] = nl2br

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Check and add missing columns safely
        with db.engine.connect() as conn:
            try:
                # First, check what columns exist
                result = conn.execute(text("PRAGMA table_info(recipes)"))
                existing_columns = [col[1] for col in result.fetchall()]
                print("\nExisting columns:", existing_columns)

                # Add missing columns if they don't exist
                if 'cook_time' not in existing_columns:
                    print("Adding cook_time column...")
                    conn.execute(text('ALTER TABLE recipes ADD COLUMN cook_time INTEGER'))
                
                if 'difficulty' not in existing_columns:
                    print("Adding difficulty column...")
                    conn.execute(text('ALTER TABLE recipes ADD COLUMN difficulty VARCHAR(20)'))
                
                if 'category_id' not in existing_columns:
                    print("Adding category_id column...")
                    conn.execute(text('ALTER TABLE recipes ADD COLUMN category_id INTEGER REFERENCES categories(id)'))
                
                conn.commit()
                print("Database update completed successfully!")

            except Exception as e:
                print(f"Error updating database: {e}")
                db.session.rollback()

    app.run(debug=True)






