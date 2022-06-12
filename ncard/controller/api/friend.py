from flask import *
import jwt
from functools import wraps
from model.db import con_pool
from time import sleep
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


@friend_blueprint.route("/api/friend", methods=["GET"])
@token_required
def cardprofile(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute(
            "SELECT friend.*,ncard.*,profile.* FROM friend INNER JOIN ncard on friend.user1=ncard.user_id INNER JOIN profile on friend.user1=profile.user_id WHERE (friend.user1=%s OR friend.user2=%s) AND (friend.friendship IS true)  UNION ALL SELECT friend.*,ncard.*,profile.* FROM friend INNER JOIN ncard on friend.user2=ncard.user_id INNER JOIN profile on friend.user2=profile.user_id WHERE (friend.user1=%s OR friend.user2=%s) AND (friend.friendship IS true)", (current_user, current_user, current_user, current_user))
        alluser = cursor.fetchall()
        if alluser:
            friend_list = []
            for index in range(len(alluser)):
                if alluser[index]['user_id'] != current_user:
                    data = {
                        "user_id": alluser[index]["user_id"],
                        "realname": alluser[index]["realname"],
                        "school": alluser[index]["school"],
                        "image": alluser[index]["image"]
                    }
                    friend_list.append(data)
            print(friend_list)
            return {"data": friend_list}
        else:
            return {"data": None}
    finally:
        cursor.close()
        db.close()
