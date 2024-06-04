from flask import Blueprint, render_template, flash, redirect, url_for, \
    abort, request
from flask_login import current_user, login_required
from cookbook.models import Recipe, RecipeIngredient, Ingredient
from cookbook.forms import RecipeForm
from cookbook.extensions import db, trim_decimals
from itertools import zip_longest

bp = Blueprint('recipes', __name__, url_prefix='/recipes',
               template_folder="templates")


@bp.route('/')
def home():
    if current_user.is_authenticated:
        recipes = Recipe.query.filter(
            (Recipe.deleted == False) &
            ((Recipe.owner == current_user) | (Recipe.public))).order_by(
            Recipe.id).all()
    else:
        recipes = Recipe.query.filter_by(public=True).order_by(Recipe.id).all()

    return render_template("recipes/list.html", recipes=recipes)


@bp.route("/add/", methods=["GET", "POST"])
@login_required
def add():
    form = RecipeForm()

    if form.validate_on_submit():
        recipe = Recipe(
            name=form.name.data, instructions=form.instructions.data,
            servings=form.servings.data, cooking_time=form.cooking_time.data,
            user_id=current_user.id)
        db.session.add(recipe)
        db.session.commit()

        for form_data in form.ingredients.data:
            if form_data["ingredient"]:
                ingredient = Ingredient.query.filter_by(
                    name=form_data["ingredient"],
                    user_id=current_user.id).first()

                if not ingredient:
                    ingredient = Ingredient(
                        name=form_data["ingredient"],
                        user_id=current_user.id)
                    db.session.add(ingredient)
                    db.session.commit()

                recipe_ingredient = RecipeIngredient(
                    recipe_id=recipe.id, ingredient_id=ingredient.id,
                    amount=form_data["amount"],
                    unit=form_data["unit"])
                db.session.add(recipe_ingredient)

        db.session.commit()
        flash("New recipe added", "success")

        return redirect(url_for("recipes.recipe", recipe_id=recipe.id), 303)

    ingredients = Ingredient.query.order_by(Ingredient.name).all()

    return render_template("recipes/add.html", form=form,
                           ingredients=ingredients)


@bp.route("/<int:recipe_id>/")
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id, deleted=False).first_or_404()

    return render_template("recipes/recipe.html", recipe=recipe)


@bp.route("/<int:recipe_id>/edit/", methods=["GET", "POST"])
@login_required
def edit(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id, deleted=False).first_or_404()

    if recipe.owner != current_user:
        abort(403)

    form = RecipeForm()

    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.servings = form.servings.data
        recipe.cooking_time = form.cooking_time.data
        recipe.instructions = form.instructions.data
        recipe.public = form.public.data

        for form_data, recipe_ingredient in zip_longest(
                form.ingredients.data, recipe.ingredients):
            if not form_data["ingredient"]:
                if recipe_ingredient:
                    db.session.delete(recipe_ingredient)
            else:
                ingredient = Ingredient.query.filter_by(
                    name=form_data["ingredient"],
                    user_id=current_user.id).first()

                if not ingredient:
                    ingredient = Ingredient(
                        name=form_data["ingredient"],
                        user_id=current_user.id)
                    db.session.add(ingredient)
                    db.session.commit()

                if recipe_ingredient is None:
                    recipe_ingredient = RecipeIngredient(
                        recipe_id=recipe.id, ingredient_id=ingredient.id,
                        amount=form_data["amount"],
                        unit=form_data["unit"])
                    db.session.add(recipe_ingredient)
                else:
                    recipe_ingredient.amount = form_data["amount"]
                    recipe_ingredient.unit = form_data["unit"]
                    recipe_ingredient.ingredient_id = ingredient.id

        db.session.commit()
        flash("Recipe has been updated", "success")
        return redirect(url_for("recipes.recipe", recipe_id=recipe.id), 303)
    elif request.method == "GET":
        for _ in range(len(recipe.ingredients)-1):
            form.ingredients.append_entry()

        for form_ingredients, ingredient in zip(
                form.ingredients, recipe.ingredients):
            form_ingredients["ingredient"].process_data(
                ingredient.ingredient.name)
            form_ingredients["amount"].data = trim_decimals(ingredient.amount)
            form_ingredients["unit"].data = ingredient.unit

        form.name.data = recipe.name
        form.servings.data = recipe.servings
        form.cooking_time.data = recipe.cooking_time
        form.instructions.process_data(recipe.instructions)
        form.public.data = recipe.public

    ingredients = Ingredient.query.order_by(Ingredient.name).all()

    return render_template(
        "recipes/edit.html", recipe=recipe, form=form, ingredients=ingredients)


@bp.route("/<int:recipe_id>/delete/")
@login_required
def delete(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)
    if not recipe:
        abort(404)

    if recipe.owner != current_user:
        abort(403)

    for recipe_ingredient in recipe.ingredients:
        db.session.delete(recipe_ingredient)

    recipe.deleted = True
    db.session.commit()

    flash(f"Recipe {recipe.name} has been deleted", "warning")

    return redirect(url_for("recipes.home"), 303)
