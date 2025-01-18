import os
from flask import Flask
from flask_migrate import Migrate
from .extensions import db, migrate, login_manager
from .config import Config

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import blueprints
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.recipe import recipe_bp
    from .routes.admin import admin_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(admin_bp)

    return app