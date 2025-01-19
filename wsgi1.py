import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import AppConfig

# Initialize SQLAlchemy before creating the app
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Get absolute path for database
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'recipes.db')

    # Load config
    app.config.from_object(AppConfig)

    # Override database URI with absolute path
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from routes.main import main_bp
    from routes.recipe import recipe_bp

    app.register_blueprint(recipe_bp)
    app.register_blueprint(main_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)