from .extensions import db, login_manager
from flask_login import UserMixin
from dataclasses import dataclass


@login_manager.user_loader
def load_user(user_id):
    if type(user_id) is tuple:
        return db.session.get(User, int(user_id[0]))
    return db.session.get(User, int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    admin = db.Column(db.Boolean, default=False)
    ingredients = db.relationship("Ingredient", backref="owner", lazy=True)
    recipes = db.relationship("Recipe", backref="owner", lazy=True)

    def get_id(self):
        return self.id


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    instructions = db.Column(db.String)
    servings = db.Column(db.Integer, default=4, nullable=False)
    public = db.Column(db.Boolean, default=False)
    ingredients = db.relationship(
        "RecipeIngredient", backref="recipe", lazy=True)


@dataclass
class Ingredient(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False, unique=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("user.id"),
        nullable=False)
    recipes = db.relationship("RecipeIngredient", backref="ingredient",
                              lazy=True)


class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"),
                          nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"),
                              nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(10))
