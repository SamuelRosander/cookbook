from flask import Blueprint, render_template, flash, url_for, redirect, \
    abort, request
from flask_login import current_user, login_required
from cookbook.forms import IngredientForm
from cookbook.models import Ingredient
from cookbook.extensions import db

bp = Blueprint(
    'ingredients', __name__, url_prefix="/ingredients",
    template_folder="templates")


@bp.route('/', methods=["GET", "POST"])
@login_required
def home():
    form = IngredientForm()

    if form.validate_on_submit():
        ingredient = Ingredient(name=form.name.data, user_id=current_user.id)
        db.session.add(ingredient)
        db.session.commit()
        flash(f"Ingredient {form.name.data} added", "success")

    ingredients = Ingredient.query.filter_by(
        user_id=current_user.id).order_by(
        Ingredient.name).all()

    return render_template(
        "ingredients/list.html", form=form, ingredients=ingredients)


@bp.route("/<int:ingredient_id>/", methods=["GET", "POST"])
@login_required
def ingredient(ingredient_id):
    ingredient = db.session.get(Ingredient, ingredient_id)
    if not ingredient:
        abort(404)

    return render_template("ingredients/ingredient.html",
                           ingredient=ingredient)


@bp.route("/<int:ingredient_id>/edit/", methods=["GET", "POST"])
@login_required
def edit(ingredient_id):
    ingredient = db.session.get(Ingredient, ingredient_id)

    if not ingredient:
        abort(404)

    if ingredient.owner != current_user:
        abort(403)

    form = IngredientForm()

    if form.validate_on_submit():
        ingredient.name = form.name.data
        db.session.commit()
        flash("Ingredient has been updated", "succes")
    elif request.method == "GET":
        form.name.data = ingredient.name

    return render_template(
        "ingredients/edit.html", ingredient=ingredient, form=form)


@bp.route("/<int:ingredient_id>/delete/")
@login_required
def delete(ingredient_id):
    ingredient = db.session.get(Ingredient, ingredient_id)
    if not ingredient:
        abort(404)

    if ingredient.owner != current_user:
        abort(403)

    if (ingredient.recipes):
        for i in ingredient.recipes:
            url = url_for('recipes.recipe', recipe_id=i.recipe.id)
            flash(
                f"{ingredient.name} is being used in recipe \
                    <a href='{url}'>{i.recipe.name}</a>",
                "error")
        return redirect(
            url_for("ingredients.edit", ingredient_id=ingredient.id), 303)

    Ingredient.query.filter_by(id=ingredient_id).delete()
    db.session.commit()

    flash(f"Ingredient {ingredient.name} has been deleted", "warning")

    return redirect(url_for("ingredients.home"), 303)
