from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from extensions import db
from routes.main import main_bp
from routes.auth import auth_bp
from routes.shopping import shopping_bp
from models.models import User
from utils.filters import nl2br

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_master.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(shopping_bp)
    
    # Register Jinja filters
    app.jinja_env.filters['nl2br'] = nl2br
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 