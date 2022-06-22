from flask import *
import model.verify
from decouple import config
import jwt
from functools import wraps


verify_blueprint = Blueprint('verify', __name__)


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


@verify_blueprint.route("/validation", methods=["POST"])
@token_required
def add_profile(current_user):
    try:
        data = request. json
        resp = model.verify.add_profile(
            current_user, data)
        return resp
    except Exception as e:
        return {"error": True}, 500


@verify_blueprint.route("/validation", methods=["GET"])
@token_required
def get_profile(current_user):
    try:
        resp = model.verify.get_profile(current_user)
        return resp
    except Exception as e:
        return {"error": True}, 500
