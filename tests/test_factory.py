from cookbook import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True,
                       "SQLALCHEMY_DATABASE_URI": "sqlite://"}).testing


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"<title>CookBook</title>" in response.data
