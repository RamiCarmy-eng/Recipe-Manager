from flask import Flask
from flask_compress import Compress
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

from config import get_config
from extensions import db, login_manager, mail, migrate, cache, scheduler
from models import User

def create_app():
    app = Flask(__name__)
    
    # Load config based on environment
    config = get_config()
    app.config.from_object(config)
    
    # Initialize Sentry in production
    if not app.debug and not app.testing:
        sentry_sdk.init(
            dsn=app.config.get('SENTRY_DSN'),
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=os.environ.get('FLASK_ENV', 'production')
        )
    
    # Initialize core extensions
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cache.init_app(app)
    scheduler.init_app(app)  # For background tasks
    
    # Initialize security extensions
    Compress(app)  # Compress responses
    if not app.debug and not app.testing:
        Talisman(app, content_security_policy=app.config['SECURE_HEADERS'])
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Set up logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/recipe_master.log', 
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
    
    # Register error handlers
    from errors import register_error_handlers
    register_error_handlers(app)
    
    # Register CLI commands
    from commands import register_commands
    register_commands(app)
    
    # Register template filters
    from filters import register_template_filters
    register_template_filters(app)
    
    # Register context processors
    from context_processors import register_context_processors
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






