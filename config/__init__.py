import os
from datetime import timedelta
from dotenv import load_dotenv
# Import specific configs
from .auth import AuthConfig
from .database import DatabaseConfig
from .logging import LoggingConfig
from .production import ProductionConfig
load_dotenv()

class Config:
    # Basic Flask config
    FLASK_APP = os.getenv('FLASK_APP', 'wsgiO.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', True)

    # Upload config
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Recipe config
    RECIPES_PER_PAGE = 12
    MAX_SHOPPING_LISTS = 10
    MAX_COMMENT_LENGTH = 1000

    def __init__(self):
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)


class AppConfig(Config, AuthConfig, DatabaseConfig, LoggingConfig):
    """Merged configuration for the application"""
    pass


# For production
class ProductionAppConfig(AppConfig, ProductionConfig):
    """Production configuration"""
    pass