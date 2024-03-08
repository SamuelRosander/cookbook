from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from cookbook.models import Meal
from cookbook.extensions import db

bp = Blueprint('menu', __name__, url_prefix='/menu',
               template_folder="templates")


@bp.route('/')
@login_required
def home():
    meals = Meal.query.filter_by(user_id=current_user.id)

    return render_template("menu/menu.html", meals=meals)


@bp.route("/add/<int:recipe_id>")
@login_required
def add(recipe_id):
    meal = Meal(recipe_id=recipe_id, user_id=current_user.id, servings=4)

    db.session.add(meal)
    db.session.commit()

    flash("Added to menu")
    return redirect(url_for('menu.home'))
