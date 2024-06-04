from flask import Flask

from .auth import auth

from .menu import menu
from .extensions import db, login_manager, trim_decimals
from .main import main
from .ingredients import ingredients
from .recipes import recipes


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile("config.py")

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(ingredients.bp)
    app.register_blueprint(recipes.bp)
    app.register_blueprint(menu.bp)

    app.register_error_handler(401, main.error)
    app.register_error_handler(403, main.error)
    app.register_error_handler(404, main.error)

    app.add_template_filter(trim_decimals)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    return app
