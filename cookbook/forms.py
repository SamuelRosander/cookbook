from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, \
    FieldList, FormField, FloatField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Optional, \
    NumberRange
from .models import Ingredient


class IngredientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_name(self, field):
        ingredient = Ingredient.query.filter(
            Ingredient.name.ilike(field.data)).first()
        if ingredient:
            raise ValidationError("Ingredient already exists")


class RecipeIngredientForm(FlaskForm):
    ingredient = StringField("Ingredient", validators=[Optional()])
    amount = FloatField("Amount", validators=[Optional()])
    unit = StringField("Unit")


class RecipeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    servings = IntegerField("No. of servings", default=4,
                            validators=[DataRequired(), NumberRange(min=0)])
    cooking_time = IntegerField("Cooking time", default=30,
                                validators=[NumberRange(min=0)])
    instructions = TextAreaField("Instructions")
    ingredients = FieldList(FormField(RecipeIngredientForm), min_entries=1)
    public = BooleanField("Public")
    submit = SubmitField("Submit")

    def validate_ingredients(self, field):
        ingredients = [i for i in field.data if i["ingredient"] is not None]

        if len(ingredients) < 1:
            raise ValidationError("Recipes require at least 1 ingredient")
