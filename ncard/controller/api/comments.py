
from flask import *
import model.comments
import controller.decorator as dec


comments_blueprint = Blueprint('comments', __name__)


@comments_blueprint.route("/comment", methods=["POST"])
@dec.token_required
def add_comment(current_user):
    try:
        data = request. json
        resp = model.comments.add_comment(data, current_user)
        return resp
    except Exception as error:
        return {'error': str(error)}, 500


@comments_blueprint.route("/comment/<id>", methods=["GET"])
def get_comment(id):
    try:
        resp = model.comments.get_comment(id)
        return resp
    except Exception as error:
        return {'error': str(error)}, 500
