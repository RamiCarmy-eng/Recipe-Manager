import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask Configuration
    FLASK_APP = os.getenv('FLASK_APP', 'wsgi.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', True)

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_PATH', 'sqlite:///recipes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))

    def __init__(self):
        # Ensure upload folder exists
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)


config = Config()
