from flask import *
import model.cardprofile
import controller.decorator as dec

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route("/profile", methods=["GET"])
@dec.token_required
def get_profile(current_user):
    try:
        resp = model.cardprofile.get_profile(
            current_user)
        return resp
    except Exception as error:
        return {'error': str(error)}, 500


@profile_blueprint.route("/profile", methods=["POST"])
@dec.token_required
def post_profile(current_user):
    try:
        data = request. json
        resp = model.cardprofile.post_profile(current_user, data)
        return resp
    except Exception as error:
        return {'error': str(error)}, 500
