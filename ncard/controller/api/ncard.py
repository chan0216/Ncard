from email import message
from flask import *
from datetime import date, datetime, time, timedelta
from functools import wraps
from decouple import config
from model.db import con_pool
import jwt


ncard_blueprint = Blueprint('ncard', __name__)


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


@ncard_blueprint.route("/api/ncard", methods=["GET"])
@token_required
def get_ncard(current_user):
    try:
        user1 = None
        user2 = None
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        today = date.today()
        print(today)
        yesterday = today - timedelta(days=1)
        print(yesterday)
        dby = yesterday - timedelta(days=1)
        cursor.execute(
            "select `user1`,`user2` from friend where (user1 = %s OR user2 =%s ) AND date=%s", (current_user, current_user, yesterday))
        user = cursor.fetchone()
        print(user)
        if user is not None:

            if user['user1'] == current_user:
                user1 = user['user1']
            else:
                user2 = user['user2']
            if user1:
                cursor.execute(
                    "select `user2`,`user1_message`,`friendship` from friend where user1 = %s AND date=%s", (current_user, yesterday))
                user1 = cursor.fetchone()
                db.commit()
                invited = True if user1["user1_message"] else False
                is_friend = True if user1["friendship"] else False
                cursor.execute(
                    "select ncard.*,profile.* from ncard INNER JOIN profile on ncard.user_id = profile.user_id where ncard.user_id=%s", (user1["user2"],))
                match_user = cursor.fetchone()

            else:
                cursor.execute(
                    "select `user1`,`user2_message`,`friendship` from friend where user2 = %s AND date=%s", (current_user, yesterday))
                user2 = cursor.fetchone()

                invited = True if user2["user2_message"] is not None else False
                is_friend = True if user2["friendship"] is not None else False
                cursor.execute(
                    "select ncard.*,profile.* from ncard INNER JOIN profile on ncard.user_id = profile.user_id where ncard.user_id=%s", (user2["user1"],))
                match_user = cursor.fetchone()

            match_user_data = {
                "invited": invited,
                "is_friend": is_friend,
                "user_id": match_user["user_id"],
                "gender": match_user["gender"],
                "image": match_user["image"],
                "school": match_user["school"],
                "realname": match_user["realname"],
                "interest": match_user["interest"],
                "club": match_user["club"],
                "course": match_user["course"],
                "country": match_user["country"],
                "worry": match_user["worry"],
                "exchange": match_user["exchange"],
                "trying": match_user["trying"],
                "date": today
            }
            return {"data": match_user_data}
        else:
            return {"data": None}
    # except:
    #     db.rollback()
    #     return {"error": True}
    finally:
        db.close()


@ncard_blueprint.route("/api/ncard", methods=["POST"])
@token_required
def post_ncard(current_user):
    try:
        data = request. json
        message = data["message"]
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        time = datetime.now()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        print(time)
        today = date.today()
        yesterday = today - timedelta(days=1)
        dby = yesterday - timedelta(days=1)
        cursor.execute(
            "select `user1` from friend where user1 = %s AND date=%s", (current_user, yesterday))
        user1 = cursor.fetchone()
        if user1:
            cursor.execute("UPDATE friend SET user1_message=%s WHERE user1=%s AND date=%s",
                           (message, current_user, yesterday))
            db.commit()
            cursor.execute(
                "select `id`,`user2`,`user2_message` from friend where user1 = %s  AND date=%s", (current_user, yesterday))
            user2 = cursor.fetchone()
            if user2["user2_message"] is not None:
                print("對方也加你喔")
                cursor.execute("UPDATE friend SET friendship=%s WHERE user1=%s AND date=%s",
                               (True, current_user, yesterday))
                cursor.execute("Insert Into message(ncard_id,user_id,message,time) Values(%s, %s, %s,%s)", (
                    user2["id"], current_user, message, now))
                cursor.execute("Insert Into message(ncard_id,user_id,message,time) Values(%s, %s, %s,%s)", (
                    user2["id"], user2["user2"], message, now))
                db.commit()
                return {"ok": True, "friend": True}
            else:
                return{"ok": True, "friend": False}
        else:
            cursor.execute("UPDATE friend SET user2_message=%s WHERE user2=%s AND date=%s",
                           (message, current_user, yesterday))
            db.commit()
            cursor.execute(
                "select `id`,`user1`,`user1_message` from friend where user2 = %s AND date=%s", (current_user, yesterday))
            user1 = cursor.fetchone()
            if user1["user1_message"] is not None:
                print("對方也加你喔")
                cursor.execute("UPDATE friend SET friendship=%s WHERE user2=%s AND date=%s",
                               (True, current_user, yesterday))
                cursor.execute("Insert Into message(ncard_id,user_id,message,time) Values(%s, %s, %s ,%s)", (
                    user1["id"], current_user, message, now))
                cursor.execute("Insert Into message(ncard_id,user_id,message,time) Values(%s, %s, %s , %s)", (
                    user1["id"], user1["user1"], message, now))
                db.commit()
                return {"ok": True, "friend": True}
            else:
                return{"ok": True, "friend": False}
    # except:
    #     db.rollback()
    #     return{"error": True}
    finally:
        cursor.close()
        db.close()


@ncard_blueprint.route("/api/ncard-verify", methods=["GET"])
@token_required
def ncard_verify(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        # 檢查填寫自我介紹了沒
        cursor.execute(
            "SELECT ncard.user_id,ncard.match_list FROM ncard where user_id=%s ", (current_user, ))
        ncard_user = cursor.fetchone()
        if ncard_user is not None:
            match_list = json.loads(ncard_user["match_list"])
        cursor.execute(
            "SELECT  profile.user_id FROM  profile where user_id=%s ", (current_user, ))
        profile_user = cursor.fetchone()

        if ncard_user is None and profile_user is None:
            return {"verify_status": "basis"}
        elif profile_user != None and ncard_user == None:
            return {"verify_status": "profile"}
        elif profile_user != None and ncard_user != None and len(match_list) == 0:
            return {"verify_status": "Ncard", "message": "還未配對"}
        else:
            return {"verify_status": "Ncard"}
    finally:
        cursor.close()
        db.close()
