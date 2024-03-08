from cookbook import create_app
from cookbook.extensions import db
from cookbook.models import User, Ingredient, Recipe, RecipeIngredient
from dotenv import load_dotenv

load_dotenv()

with create_app().app_context():
    db.drop_all()
    db.create_all()

    db.session.add(User(id=1, email="s.rosander@gmail.com", admin=True))

    db.session.commit()

    db.session.add(
        Recipe(
            name="Spaghetti och köttfärssås",
            user_id=1,
            public=True,
            instructions="Rör ihop allt."))

    db.session.add(Ingredient(name="Blandfärs", user_id=1))
    db.session.add(Ingredient(name="Spaghetti", user_id=1))
    db.session.add(Ingredient(name="Krossade tomater", user_id=1))
    db.session.add(Ingredient(name="Gul lök", user_id=1))
    db.session.add(Ingredient(name="Tomatpuré", user_id=1))
    db.session.add(Ingredient(name="Grönsaksbuljong", user_id=1))

    db.session.add(RecipeIngredient(recipe_id=1, ingredient_id=1, amount="500", unit="g"))
    db.session.add(RecipeIngredient(recipe_id=1, ingredient_id=2, amount="500", unit="g"))
    db.session.add(RecipeIngredient(recipe_id=1, ingredient_id=3, amount="1", unit="paket"))
    db.session.add(RecipeIngredient(recipe_id=1, ingredient_id=4, amount="2", unit="st"))
    db.session.add(RecipeIngredient(recipe_id=1, ingredient_id=5, amount="1", unit="msk"))
    db.session.add(RecipeIngredient(recipe_id=1, ingredient_id=6, amount="1", unit="st"))

    db.session.add(Recipe(
            name="Krämig pasta med kycklinglårfilé och basilika",
            user_id=1,
            public=True,
            instructions="Gör det gott."))

    db.session.add(Ingredient(name="Kycklinglårfilé", user_id=1))
    db.session.add(Ingredient(name="Vitlöksklyfta", user_id=1))
    db.session.add(Ingredient(name="Vispgrädde", user_id=1))
    db.session.add(Ingredient(name="Mjölk", user_id=1))
    db.session.add(Ingredient(name="Majsstärkelse", user_id=1))
    db.session.add(Ingredient(name="Basilika", user_id=1))
    db.session.add(Ingredient(name="Soltorkade tomater", user_id=1))
    db.session.add(Ingredient(name="Rödlök", user_id=1))
    db.session.add(Ingredient(name="Körsbärstomater", user_id=1))
    db.session.add(Ingredient(name="Tagliatelle", user_id=1))

    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=7, amount="600", unit="g"))
    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=8, amount="1", unit="st"))
    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=9, amount="2.5", unit="dl"))
    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=10, amount="1", unit="dl"))
    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=11, amount="1", unit="msk"))
    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=12, amount="1",unit="kruka"))
    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=13, amount="200", unit="g"))
    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=14, amount="1", unit="st"))
    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=15, amount="250", unit="g"))
    db.session.add(RecipeIngredient(recipe_id=2, ingredient_id=16, amount="500", unit="g"))


    db.session.commit()
