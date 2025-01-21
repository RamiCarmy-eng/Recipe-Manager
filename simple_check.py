from flask import Flask
from extensions import db
from models.models import User, Recipe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    users = User.query.all()
    recipes = Recipe.query.all()
    print(f"\nNumber of users: {len(users)}")
    print(f"Number of recipes: {len(recipes)}")
    
    if users:
        print(f"\nFirst user: {users[0].username}")
    if recipes:
        print(f"First recipe: {recipes[0].name}") 