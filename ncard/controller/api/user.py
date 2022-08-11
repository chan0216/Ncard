from flask_bcrypt import Bcrypt
from flask import *
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import datetime
from decouple import config
import model.user


user_blueprint = Blueprint('user', __name__)
bcrypt = Bcrypt()


@user_blueprint.route("/user", methods=["POST"])
def user_signin():
    data = request. json
    # 使用google登入
    if data['signintype'] == "Google":
        google_token = data["id_token"]
        id_info = id_token.verify_oauth2_token(google_token, requests.Request(
        ), "312350990373-e5rs7t2t9oomvbdrckop2sto4ijbpea3.apps.googleusercontent.com")
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return {"Error": True, "message": "Wrong issuer"}, 403
        if id_info["aud"] != "312350990373-e5rs7t2t9oomvbdrckop2sto4ijbpea3.apps.googleusercontent.com":
            return {"Error": True, "message": "Could not verify audience"}, 403
        else:
            username = id_info["sub"]

    # 原生系統登入
    else:
        username = data['email']
        password = data['password']

    try:
        resp = model.user.check_user(
            username)
        if resp:
            payload = {
                "user_id": resp["user_id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=300)
            }
            if resp["password"]:
                if resp["password"] != password:
                    res = make_response(
                        jsonify({"error": True, "message": "登入失敗,請重新嘗試"}), 400)
                    return res

            token = jwt.encode(payload, config(
                "secret_key"), algorithm='HS256')
            res = make_response(jsonify({"ok": True}), 200)
            res.set_cookie('token', token, expires=datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=300))
            return res

        else:
            resp = model.user.create_user(username, password)
            payload = {
                "user_id":  resp["user_id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=300)
            }
            token = jwt.encode(payload, config(
                "secret_key"), algorithm='HS256')
            res = make_response(jsonify({"ok": True}), 200)
            res.set_cookie('token', token, expires=datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=300))
            return res
    except Exception as error:
        return {'error': str(error)}, 500


@user_blueprint.route("/user", methods=["GET"])
def get_user():
    token = request.cookies.get('token')
    if token is not None:
        user_data = jwt.decode(token.encode('UTF-8'),
                               config("secret_key"), algorithms=["HS256"])
        if user_data:
            return {"ok": True}
    else:
        return {"data": None}


@user_blueprint.route("/user", methods=["DELETE"])
def delete_user():
    res = make_response(jsonify({"ok": True}), 200)
    res.delete_cookie("token")
    return res
