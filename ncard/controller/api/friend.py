from flask import *
import jwt
from functools import wraps
import model.friend
from decouple import config


friend_blueprint = Blueprint("friend", __name__)


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


@friend_blueprint.route("/friend", methods=["GET"])
@token_required
def get_all_friends(current_user):
    try:
        resp = model.friend.get_all_friends(
            current_user)
        return resp
    except:
        return {"error": True}, 500


@friend_blueprint.route("/friend/<id>", methods=["GET"])
def get_friend(id):
    try:
        token = request.cookies.get('token')
        if token:
            jwtdata = jwt.decode(token.encode('UTF-8'),
                                 config("secret_key"), algorithms=["HS256"])
            current_user = jwtdata["user_id"]
        resp = model.friend.get_friend(id, current_user)
        return resp
    except:
        return {"error": True}, 500
