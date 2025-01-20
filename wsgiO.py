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


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    # Set configuration
    app.config.update(config)


    # Initialize extensions
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

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        with app.app_context():
            # Debug: Print table structure
            with db.engine.connect() as conn:
                # Check recipes table structure
                result = conn.execute(text("PRAGMA table_info(recipes)"))
                columns = result.fetchall()
                print("\nRecipes Table Structure:")
                for col in columns:
                    print(f"Column: {col}")

        db.create_all()

        # Add new column if it doesn't exist
        from models.models import Recipe
        with db.engine.connect() as conn:
            try:
                # Check if column exists first
                result = conn.execute(text("PRAGMA table_info(recipes)"))
                columns = [col[1] for col in result.fetchall()]

                if 'subcategory' not in columns:
                    conn.execute(text('ALTER TABLE recipes ADD COLUMN subcategory VARCHAR(100)'))
                    conn.commit()
                    print("Added subcategory column successfully")
                else:
                    print("Subcategory column already exists")

            except Exception as e:
                print(f"Error checking/adding column: {e}")
                db.session.rollback()

    app.run(debug=True)






