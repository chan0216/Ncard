from flask import *
from functools import wraps
from decouple import config
import model.cardprofile
import jwt
profile_blueprint = Blueprint('profile', __name__)


def token_required(f):
    @wraps(f)
    def decorated():
        token = request.cookies.get('token')
        if not token:
            res = make_response(
                jsonify({"error": True, "message": "未登入系統，拒絕存取"}), 403)
            return res
        try:
            jwtdata = jwt.decode(token.encode('UTF-8'),
                                 config("secret_key"), algorithms=["HS256"])
            current_user = jwtdata["user_id"]
        except Exception as e:
            res = make_response(
                jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
            return res

        return f(current_user)
    return decorated


@profile_blueprint.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    try:
        resp = model.cardprofile.get_profile(
            current_user)
        return resp
    except Exception as e:
        return {"error": True}, 500


@profile_blueprint.route("/profile", methods=["POST"])
@token_required
def post_profile(current_user):
    try:
        data = request. json
        resp = model.cardprofile.post_profile(current_user, data)
        return resp
    except Exception as e:
        return {"error": True}, 500
