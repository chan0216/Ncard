from flask import *
from decouple import config
from model.db import con_pool
import jwt
from functools import wraps
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


@profile_blueprint.route("/api/profile", methods=["POST"])
@token_required
def post_profile(current_user):
    try:
        data = request. json
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT  `userID` from profile WHERE userID = %s", (current_user,))
        user_profile = cursor.fetchone()
        if user_profile is None:
            cursor.execute("Insert Into profile(userID ,realname ,gender ,school) Values( %s, %s ,%s ,%s)",
                           (current_user, data["realname"], data["gender"], data["school"]))
            db.commit()
            return {"ok": True}
        else:
            return {"error": True, "message": "重複的資料"}, 400
    except:
        db.rollback()
    finally:
        db.close()


@profile_blueprint.route("/api/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT `gender`,`school` from profile WHERE userID = %s", (current_user,))
        user_profile = cursor.fetchone()
        if user_profile is not None:
            return {"data": user_profile}
        else:
            return {"error": True, "message": "還沒填寫基本資料"}
    finally:
        db.close()
