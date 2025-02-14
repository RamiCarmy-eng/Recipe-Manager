from flask import Flask
# Standard library imports
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

# Security extensions
from flask_compress import Compress
from flask import Flask, current_app
from flask_login import current_user
from flask_compress import Compress
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Get base directory
basedir = Path(__file__).parent

# Core extensions
from extensions import (
    db,
    login_manager,
    mail,
    migrate,
    cache,
    scheduler
)
# Local imports - models
from models import User

# Local imports - utils
from errors import register_error_handlers
from filters import register_template_filters
from context_processors import register_context_processors

# Local imports - routes
from routes.auth import auth_bp
from routes.main import main_bp
from routes.recipe import recipe_bp
from routes.api import api_bp
from routes.admin import admin_bp
from routes.shopping import shopping_bp
from routes.user import user_bp
from routes.category import category_bp
from routes.favorite import favorite_bp
from routes.comment import comment_bp
from routes.search import search_bp
from routes.export import export_bp
from routes.notification import notification_bp
from routes.collaboration import collab_bp


def register_commands(app):
    @app.cli.command('init-db')
    def init_db():
        """Initialize the database."""
        db.create_all()
        click.echo('Initialized the database.')


def create_app():
    app = Flask(__name__)

    # Set secret key directly first
    app.secret_key = 'dev'

    # Set database URI directly
    basedir = Path(__file__).parent
    # Ensure instance folder exists
    instance_path = Path(basedir, 'instance')
    db_path = Path(instance_path, 'recipes.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Load config directly from Config class
    from config import Config
    app.config.from_object(Config)

    # Ensure instance folder exists
    if not instance_path.exists():
        instance_path.mkdir(parents=True)

    # Initialize core extensions
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize mail with explicit debug setting
    app.config['MAIL_DEBUG'] = int(app.config.get('MAIL_DEBUG', 0))
    mail.init_app(app)

    cache.init_app(app)
    scheduler.init_app(app)
    
    # Initialize security extensions
    Compress(app)
    if not app.debug and not app.testing:
        Talisman(app, content_security_policy=app.config.get('SECURE_HEADERS', {}))
        
        # Initialize Sentry
        if app.config.get('SENTRY_DSN'):
            sentry_sdk.init(
                dsn=app.config['SENTRY_DSN'],
                integrations=[FlaskIntegration()],
                traces_sample_rate=1.0,
                environment=os.environ.get('FLASK_ENV', 'production')
            )
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Set up logging
    if not app.debug and not app.testing:
        logs_dir = Path(app.root_path) / 'logs'
        logs_dir.mkdir(exist_ok=True)
        
        file_handler = RotatingFileHandler(
            str(logs_dir / 'recipe_master.log'),
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Recipe Master startup')
    
    # Register all blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp, url_prefix='/recipe')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(shopping_bp, url_prefix='/shopping')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(category_bp, url_prefix='/category')
    app.register_blueprint(favorite_bp, url_prefix='/favorite')
    app.register_blueprint(comment_bp, url_prefix='/comment')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(export_bp, url_prefix='/export')
    app.register_blueprint(notification_bp, url_prefix='/notification')
    app.register_blueprint(collab_bp, url_prefix='/collab')
    
    # Register error handlers, commands, filters, and context processors
    register_error_handlers(app)
    register_commands(app)
    register_template_filters(app)
    register_context_processors(app)
    
    # Register Jinja2 extensions
    app.jinja_env.add_extension('jinja2.ext.do')
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    
    @login_manager.user_loader
    def load_user(user_id):
        if user_id is None:
            return None
        return User.query.get(int(user_id))
    
    # Before request handlers
    @app.before_request
    def before_request():
        from flask_login import current_user
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()
    
    # Start scheduled tasks
    with app.app_context():
        scheduler.start()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()






