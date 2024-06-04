from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from functools import wraps
from flask import abort

db = SQLAlchemy()
login_manager = LoginManager()


def trim_decimals(num):
    if num is None:
        return ""
    inum = int(num)
    return (num if num != inum else inum)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or not current_user.admin:
            abort(403)

        return f(*args, **kwargs)
    return decorated_function
