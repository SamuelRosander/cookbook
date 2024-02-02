from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, \
    FieldList, SelectField, FormField, FloatField, BooleanField
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
    ingredient = SelectField("Ingredient", default=0)
    amount = FloatField("Amount", validators=[Optional()])
    unit = StringField("Unit")

    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        self.ingredient.choices = [(0, "--- Choose an ingredient ---")]
        self.ingredient.choices += [
            (i.id, i.name)
            for i in Ingredient.query.order_by(Ingredient.name).all()]


class RecipeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    servings = IntegerField("No. of servings", default=4,
                            validators=[DataRequired(), NumberRange(min=0)])
    instructions = TextAreaField("Instructions")
    ingredients = FieldList(FormField(RecipeIngredientForm), min_entries=1)
    public = BooleanField("Public")
    submit = SubmitField("Submit")

    def validate_ingredients(self, field):
        ingredients = [i for i in field.data if i["ingredient"] != "0"]

        if len(ingredients) < 1:
            raise ValidationError("Recipes require at least 1 ingredient")
