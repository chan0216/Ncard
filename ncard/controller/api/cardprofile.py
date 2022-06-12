from email import message
from flask import *
from functools import wraps
from decouple import config
from model.db import con_pool
import jwt
cardprofile_blueprint = Blueprint('cardprofile', __name__)


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


@cardprofile_blueprint.route("/api/cardprofile", methods=["GET"])
@token_required
def get_cardprofile(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "select ncard.*,profile.* from ncard INNER JOIN profile on ncard.user_id = profile.user_id where ncard.user_id=%s", (current_user,))
        user = cursor.fetchone()
        if user:

            # 做到這邊
            # data = {
            #     "user_id": user["user_id"],
            #     "image": user["image"],
            #     "interest": user["interest"],
            #     "club": user["club"],
            #     "course": user["course"]
            # }
            return {"data": user}
        else:
            return {"data": None}
    finally:
        cursor.close()
        db.close()


@cardprofile_blueprint.route("/api/cardprofile", methods=["POST"])
@token_required
def cardprofile(current_user):
    try:
        data = request. json
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "select user_id from ncard where user_id=%s", (current_user,))
        result = cursor.fetchone()

        if result is None:
            sql = "INSERT INTO ncard(user_id, image,  interest, club, course, country, worry, exchange, trying ,match_list) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (current_user, data["ncardImage"], data["interest"], data["club"], data["course"],
                   data["country"], data["worry"], data["exchange"], data["trying"], '[]')
            cursor.execute(sql, val)
        else:
            cursor.execute(
                "UPDATE ncard SET image=%s,interest=%s,club=%s,course=%s,country=%s, worry=%s, exchange=%s,trying=%s  where user_id=%s", (data["ncardImage"], data["interest"], data["club"], data["course"],
                                                                                                                                          data["country"], data["worry"], data["exchange"], data["trying"], current_user))
        return {"ok": True}
    # except:
    #     db.rollback()
    #     return{"error": True, "message": "伺服器內部錯誤"},500
    finally:
        db.commit()
        cursor.close()
        db.close()
