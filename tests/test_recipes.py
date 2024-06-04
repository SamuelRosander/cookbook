from cookbook.models import Recipe, User
from cookbook.extensions import db
from flask_login import login_user, logout_user


def test_home(client):
    response = client.get("/recipes/")

    assert response.status_code == 200
    assert b"<title>CookBook</title>" in response.data


def test_add(client, app):
    response = client.get("/recipes/add/")
    assert response.status_code == 401

    with app.test_request_context():
        login_user(db.session.get(User, 1))

        response = client.get("/recipes/add/")
        assert response.status_code == 200
        assert b'id="ingredients-0-ingredient"' in response.data

        client.post("/ingredients/", data={"name": "testingredient1"})
        response = client.post(
            "/recipes/add/",
            data={"name": "testrecipe1", "ingredients-0-ingredient": 1})

        assert response.status_code == 303
        assert Recipe.query.count() == 1
        assert Recipe.query.first().id == 1
        assert Recipe.query.first().name == "testrecipe1"


def test_recipe(client, app):
    with app.test_request_context():
        login_user(db.session.get(User, 1))

        client.post("/ingredients/", data={"name": "testingredient1"})
        client.post(
            "/recipes/add/",
            data={"name": "testrecipe1", "ingredients-0-ingredient": 1})

        response = client.get("/recipes/1/")
        assert response.status_code == 200
        assert b"<h3>testrecipe1</h3>" in response.data

        assert client.get("/recipes/2/").status_code == 404


def test_edit(client, app):
    with app.test_request_context():
        login_user(db.session.get(User, 1))

        client.post("/ingredients/", data={"name": "testingredient1"})
        client.post(
            "/recipes/add/",
            data={"name": "testrecipe1", "ingredients-0-ingredient": 1})

        response = client.get("/recipes/1/edit/")
        assert response.status_code == 200
        assert b'value="testrecipe1"' in response.data
        assert b'testingredient1' in response.data

        response = client.post(
            "/recipes/1/edit/",
            data={"name": "testedited", "ingredients-0-ingredient": 1})
        assert response.status_code == 303

        response = client.get("/recipes/1/edit/")
        assert b'value="testedited"' in response.data

        assert client.get("/recipes/2/edit/").status_code == 404


def test_delete(client, app):
    with app.test_request_context():
        login_user(db.session.get(User, 1))

        client.post("/ingredients/", data={"name": "testingredient1"})
        client.post(
            "/recipes/add/",
            data={"name": "testrecipe1", "ingredients-0-ingredient": 1})

        logout_user()

        assert client.get("/recipes/1/delete/").status_code == 401
        assert client.get("/recipes/2/delete/").status_code == 401

        login_user(db.session.get(User, 1))

        assert client.get("/recipes/1/delete/").status_code == 303
        assert client.get("/recipes/2/delete/").status_code == 404
