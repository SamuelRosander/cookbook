from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template("index.html")


def error(error):
    return render_template("error.html", error=error), error.code
