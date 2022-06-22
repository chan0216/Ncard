from email import message
from flask import *
from datetime import date, datetime, time, timedelta
from functools import wraps
from decouple import config
from model.db import con_pool
import model.ncard
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


@ncard_blueprint.route("/ncard", methods=["GET"])
@token_required
def get_ncard(current_user):
    try:
        today = date.today()
        yesterday = today - timedelta(days=1)
        resp = model.ncard.get_ncard(
            current_user, today, yesterday)
        return resp
    except:
        return {"error": True}, 500


@ncard_blueprint.route("/ncard", methods=["POST"])
@token_required
def create_ncard(current_user):
    try:
        data = request. json
        message = data["message"]
        time = datetime.now()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        today = date.today()
        yesterday = today - timedelta(days=1)
        resp = model.ncard.create_ncard(
            current_user, yesterday, now, message)
        return resp
    except:
        return {"error": True}, 500


@ncard_blueprint.route("/status", methods=["GET"])
@token_required
def user_status(current_user):
    try:
        resp = model.ncard.user_status(current_user)
        return resp
    except:
        return {"error": True}, 500
