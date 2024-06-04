from .extensions import db, login_manager
from flask_login import UserMixin
from dataclasses import dataclass
from datetime import datetime


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
    meals = db.relationship("Meal", backref="owner", lazy=True)

    def get_id(self):
        return self.id


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    instructions = db.Column(db.String)
    servings = db.Column(db.Integer, default=4, nullable=False)
    cooking_time = db.Column(db.Integer, default=30)
    public = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)
    ingredients = db.relationship(
        "RecipeIngredient", backref="recipe", lazy=True)
    meals = db.relationship("Meal", backref="recipe", lazy=True)


@dataclass
class Ingredient(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False, unique=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False)
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


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    recipes = db.relationship("RecipeTag", backref="tag",
                              lazy=True)


class RecipeTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"),
                          nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"),
                       nullable=False)


class Appliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    recipes = db.relationship("RecipeAppliance", backref="appliance",
                              lazy=True)


class RecipeAppliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"),
                          nullable=False)
    appliance_id = db.Column(db.Integer, db.ForeignKey("appliance.id"),
                             nullable=False)


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(
        db.Integer, db.ForeignKey("recipe.id"),
        nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow())
    servings = db.Column(db.Integer, nullable=False)
