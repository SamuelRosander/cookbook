from cookbook.models import Ingredient, User
from cookbook.extensions import db
from flask_login import login_user, logout_user


def test_home(client, app):
    assert client.get("/ingredients/").status_code == 401

    with app.test_request_context():
        login_user(db.session.get(User, 1))

        response = client.get("/ingredients/")
        assert response.status_code == 200
        assert b"<h3>Add ingredient</h3>" in response.data


def test_add(client, app):
    response = client.post("/ingredients/", data={"name": "testingredient1"})

    assert response.status_code == 401

    with app.test_request_context():
        assert Ingredient.query.count() == 0

        login_user(db.session.get(User, 1))

        response = client.post(
            "/ingredients/", data={"name": "testingredient2"})
        assert response.status_code == 200
        assert Ingredient.query.count() == 1
        assert Ingredient.query.first().id == 1
        assert Ingredient.query.first().name == "testingredient2"


def test_edit(client, app):
    with app.test_request_context():
        login_user(db.session.get(User, 1))

        client.post("/ingredients/", data={"name": "testingredient1"})

        response = client.get("/ingredients/1/edit/")
        assert response.status_code == 200
        assert b"<h3>Edit ingredient</h3>" in response.data
        assert b'value="testingredient1"' in response.data

        client.post("/ingredients/1/edit/",
                    data={"name": "testingredient1edit"})

        response = client.get("/ingredients/1/edit/")
        assert b'value="testingredient1edit"' in response.data
        assert client.get("/ingredients/2/edit/").status_code == 404

        logout_user()

        response = client.get("/ingredients/1/edit/")
        assert response.status_code == 401

        client.post("/ingredients/1/edit/",
                    data={"name": "testingredient1edit2"})

        response = client.get("/ingredients/1/edit/")
        assert response.status_code == 401


def test_delete(client, app):
    with app.test_request_context():
        login_user(db.session.get(User, 1))
        client.post("/ingredients/", data={"name": "testingredient1"})
        client.post("/ingredients/", data={"name": "testingredient2"})

        client.post(
            "/recipes/add/",
            data={"name": "testrecipe1",
                  "ingredients-0-ingredient": "testingredient1"})

        assert client.get("/ingredients/3/delete/").status_code == 404

        response = client.get("/ingredients/1/delete/")
        assert response.status_code == 303
        assert Ingredient.query.count() == 2

        response = client.get("/ingredients/2/delete/")
        assert response.status_code == 303
        assert Ingredient.query.count() == 1

        logout_user()

        response = client.get("/ingredients/2/delete/")
        assert response.status_code == 401
        assert Ingredient.query.count() == 1
