import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logging(app):
    # Set up logging to file
    file_handler = RotatingFileHandler(
        'logs/recipe_manager.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Set up logging to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    console_handler.setLevel(logging.INFO)
    app.logger.addHandler(console_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Recipe Manager startup') 