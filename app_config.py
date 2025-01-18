import os

# Get the absolute path of the project directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration dictionary
config = {
    'SECRET_KEY': 'your-secret-key-here',
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///instance/recipes.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    
    # Image folder settings - ONLY using static/images
    'UPLOAD_FOLDER': os.path.join(basedir, 'static', 'images'),
    'AVATAR_FOLDER': os.path.join(basedir, 'static', 'images', 'avatars'),
    'RECIPE_FOLDER': os.path.join(basedir, 'static', 'images', 'recipes'),
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max file size
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'gif'},
}

# Create folders if they don't exist
def create_upload_folders():
    folders = [
        config['UPLOAD_FOLDER'],    # /static/images
        config['AVATAR_FOLDER'],    # /static/images/avatars
        config['RECIPE_FOLDER'],    # /static/images/recipes
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")