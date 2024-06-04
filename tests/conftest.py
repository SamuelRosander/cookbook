import pytest
from cookbook import create_app, db
from cookbook.models import User


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "testing",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        db.session.add(User(email='test@url.test'))
        db.session.add(User(email='test2@url.test'))
        db.session.commit()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
