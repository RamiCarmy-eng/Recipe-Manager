from datetime import datetime
from flask_login import UserMixin
from extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

class Comment(db.Model):
    __tablename__ = 'comments'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    recipes = db.relationship('Recipe', back_populates='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    shopping_lists = db.relationship('ShoppingList', backref='user', lazy=True)
    activities = db.relationship('UserActivity', backref='user', lazy=True)

    preference = db.relationship('UserPreference', backref='qwner', uselist=False)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email_notifications = db.Column(db.Boolean, default=True)
    public_profile = db.Column(db.Boolean, default=False)
    default_servings = db.Column(db.Integer, default=4)
    measurement_system = db.Column(db.String(10), default='metric')  # 'metric' or 'imperial'
    theme = db.Column(db.String(20), default='light')  # 'light' or 'dark'
    language = db.Column(db.String(5), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with User
    #user = db.relationship('User', backref=db.backref('preferences', uselist=False))

    def __repr__(self):
        return f'<UserPreference {self.user_id}>'

    @property
    def is_active(self):
        return True  # You can add logic here if needed

    @property
    def is_authenticated(self):
        return True  # You can add logic here if needed

    @property
    def is_anonymous(self):
        return False


class Recipe(db.Model):
    __tablename__ = 'recipes'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.Column(db.String(100))
    subcategory = db.Column(db.String(100))

    # Boolean flags
    is_reported = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_hidden = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    rejection_reason = db.Column(db.String(255))

    # Relationships
    user = db.relationship('User', back_populates='recipes')  # Matches User model's recipes relationship
    category = db.relationship('Category', backref='recipes', lazy=True)
    ingredients = db.relationship('RecipeIngredient', backref='recipe',
                                  cascade='all, delete-orphan')  # Links to RecipeIngredient model
    comments = db.relationship('Comment', backref='recipe', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='recipe', cascade='all, delete-orphan')


    # Hybrid property to handle both name and title
    @hybrid_property
    def title(self):
        return self.name

    @title.setter
    def title(self, value):
        self.name = value


    def __repr__(self):
        return f'<Recipe {self.name}>'

class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(50))
    description = db.Column(db.Text)
    category = db.Column(db.String(100))

    def __repr__(self):
        return f'<Ingredient {self.name}>'


class Favorite(db.Model):
    __tablename__ = 'favorites'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)  # Changed from recipes_images
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class IngredientCategory(db.Model):
    __tablename__ = 'ingredient_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='ingredient_categories')


class ShoppingList(db.Model):
    __tablename__ = 'shopping_lists'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ShoppingListItem(db.Model):
    __tablename__ = 'shopping_list_items'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_lists.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    ingredient_name = db.Column(db.String(100), nullable=False)  # Add this line
    amount = db.Column(db.Float)
    unit = db.Column(db.String(20))
    checked = db.Column(db.Boolean, default=False)

class ShoppingListTemplate(db.Model):
    __tablename__ = 'shopping_list_templates'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    items = db.relationship('TemplateItem', backref='template', lazy=True)
    user = db.relationship('User', backref='shopping_templates', lazy=True)


class TemplateItem(db.Model):
    __tablename__ = 'template_items'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('shopping_list_templates.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(50))
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class CollaborativeList(db.Model):
    __tablename__ = 'collaborative_lists'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    owner = db.relationship('User', backref='owned_lists', lazy=True)
    items = db.relationship('CollaborativeListItem', backref='list', lazy=True)
    members = db.relationship('CollaborativeListMember', backref='list', lazy=True)


class CollaborativeListMember(db.Model):
    __tablename__ = 'collaborative_list_members'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('collaborative_lists.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    can_edit = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='list_memberships', lazy=True)


class CollaborativeListItem(db.Model):
    __tablename__ = 'collaborative_list_items'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('collaborative_lists.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(50))
    category = db.Column(db.String(50))
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    adder = db.relationship('User', foreign_keys=[added_by], backref='added_items', lazy=True)
    completer = db.relationship('User', foreign_keys=[completed_by], backref='completed_items', lazy=True)


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)  # Changed from recipes_images
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(20))


class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserActivity {self.action}>'
