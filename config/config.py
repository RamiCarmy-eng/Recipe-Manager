import os


class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///recipes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for session management
    SECRET_KEY = 'dev'

    # Upload folder for images
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


config = Config()
