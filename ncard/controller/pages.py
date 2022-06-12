from crypt import methods
from flask import Blueprint

pages = Blueprint("pages", __name__)


@pages.route("/", methods=["GET"])
def index():
    pass
