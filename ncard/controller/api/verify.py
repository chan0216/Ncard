from flask import *
import model.verify
import controller.decorator as dec

verify_blueprint = Blueprint('verify', __name__)


@verify_blueprint.route("/validation", methods=["POST"])
@dec.token_required
def add_profile(current_user):
    try:
        data = request. json
        resp = model.verify.add_profile(
            current_user, data)
        return resp
    except Exception as e:
        return {"error": True}, 500


@verify_blueprint.route("/validation", methods=["GET"])
@dec.token_required
def get_profile(current_user):
    try:
        resp = model.verify.get_profile(current_user)
        return resp
    except Exception as e:
        return {"error": True}, 500
