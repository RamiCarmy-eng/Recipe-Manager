import os

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(test_config=None):
    # Create Flask app
    app = Flask(__name__, instance_relative_config=True)

    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'recipes_images.db'),
        UPLOAD_FOLDER=os.path.join(app.static_folder, 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'}
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('app_config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ensure the uploads folder exists
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    # Initialize database
    from .database import init_app
    init_app(app)

    # Register error handlers
    from .error_handlers import register_error_handlers
    register_error_handlers(app)

    # Register logging
    from .logging import setup_logging
    setup_logging(app)

    # Add proxy fix for running behind reverse proxy
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    return app
