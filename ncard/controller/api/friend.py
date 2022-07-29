from flask import *
import jwt
import model.friend
from decouple import config
import controller.decorator as dec


friend_blueprint = Blueprint("friend", __name__)


@friend_blueprint.route("/friend", methods=["GET"])
@dec.token_required
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
