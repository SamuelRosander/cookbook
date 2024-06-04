from flask import Blueprint, render_template

bp = Blueprint('main', __name__, template_folder="templates")


@bp.route('/')
def index():
    return render_template("main/index.html")


def error(error):
    return render_template("main/error.html", error=error), error.code
