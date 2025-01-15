from extensions import db


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    instructions = db.Column(db.Text)
    image = db.Column(db.String(200))

    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
