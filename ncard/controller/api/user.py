from flask import current_app
from flask_bcrypt import Bcrypt
from flask import *
from google.oauth2 import id_token
from google.auth.transport import requests
from flask_mail import Mail, Message
from model.db import con_pool
import jwt
import datetime
# from redis import Redis
# from rq import Queue
from decouple import config
from itsdangerous import SignatureExpired, URLSafeTimedSerializer


user_blueprint = Blueprint('user', __name__)

bcrypt = Bcrypt()


# def send_email(token):
#     try:
#         msg_title = 'Ncard 註冊認證信'
#         sender = config('MAIL_USERNAME')
#         msg_recipients = [config('MAIL_USERNAME')]
#         link = url_for("user.confirm_email",
#                        token=token, _external=True)
#         msg_html = f"<h3>感謝你註冊Ncard</h3><p>現在點擊下方連結完成驗證，即可馬上啟用完整功能喔！</p>{link}"
#         msg = Message(msg_title, sender=sender,
#                       recipients=msg_recipients)
#         msg.html = msg_html
#         with current_app.app_context():
#             mail = Mail()
#             mail.send(msg)
#         return "ok"
#     except:
#         return "error"


# def generate_confirmation_token(email):
#     serializer = URLSafeTimedSerializer(config('SECRET_KEY'))
#     return serializer.dumps(email, salt=config('SECURITY_PASSWORD_SALT'))


# def confirm_token(token, expiration=3600):
#     serializer = URLSafeTimedSerializer(config('SECRET_KEY'))
#     try:
#         email = serializer.loads(
#             token,
#             salt=config('SECURITY_PASSWORD_SALT'),
#             max_age=expiration
#         )
#     except:
#         return False
#     return email


@user_blueprint.route("/api/user", methods=["POST"])
def signin():
    FB_id = None
    Google_id = None
    data = request. json
    # 使用google登入
    if data['signintype'] == "Google":
        token = data["id_token"]
        id_info = id_token.verify_oauth2_token(token, requests.Request(
        ), "312350990373-e5rs7t2t9oomvbdrckop2sto4ijbpea3.apps.googleusercontent.com")
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return {"Error": True, "message": "Wrong issuer"}, 403
        if id_info["aud"] != "312350990373-e5rs7t2t9oomvbdrckop2sto4ijbpea3.apps.googleusercontent.com":
            return {"Error": True, "message": "Could not verify audience"}, 403
        else:
            username = id_info["sub"]

    # 使用fb登入
    elif data['signintype'] == "FB":

        username = data["username"]
        # user_email = data["email"]

    # 原生系統登入
    else:
        username = data['email']
        password = data['password']
        hashed_password = bcrypt.generate_password_hash(
            password=password).decode('utf-8')

    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT  * from user WHERE username  = %s ", (username,))
        user = cursor.fetchone()
        if user is None:
            if data['signintype'] == "Google":
                sql = "Insert Into user(username,signintype) Values(%s,%s)"
                val = (username, "Google")
                cursor.execute(sql, val)
                cursor.execute(
                    "SELECT  `user_id` from user WHERE username = %s", (username,))
                user_id = cursor.fetchone()
                payload = {
                    "user_id":  user_id["user_id"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
                }
                token = jwt.encode(payload, config(
                    "secret_key"), algorithm='HS256')
                res = make_response(jsonify({"ok": True}), 200)
                res.set_cookie('token', token, expires=datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=180))
                return res
            elif data['signintype'] == "FB":
                sql = "Insert Into user(username,signintype) Values( %s,%s)"
                val = (username, "FB")
                cursor.execute(sql, val)
                cursor.execute(
                    "SELECT  `user_id` from user WHERE username = %s", (username,))
                user_id = cursor.fetchone()
                payload = {
                    "user_id":  user_id["user_id"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
                }
                token = jwt.encode(payload, config(
                    "secret_key"), algorithm='HS256')
                res = make_response(jsonify({"ok": True}), 200)
                res.set_cookie('token', token, expires=datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=180))
                return res
            else:
                # token = generate_confirmation_token(username)
                # send_status = send_email(token)
                # if send_status == "ok":
                # sql = "Insert Into unconfirmeduser(email,password) Values( %s ,%s)"
                # val = (username, hashed_password)
                # cursor.execute(sql, val)
                # payload = {
                #     "user_email": username,
                #     "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
                # }
                # unconfirmed = jwt.encode(payload, config(
                #     "secret_key"), algorithm='HS256')
                # res = make_response(
                #     jsonify({"ok": True, "message": "驗證信發送成功"}), 200)
                # res.set_cookie('unconfirmed', unconfirmed, expires=datetime.datetime.utcnow(
                # ) + datetime.timedelta(minutes=180))
                # return res
                sql = "Insert Into user(username,password,signintype) Values( %s,%s,%s)"
                val = (username, hashed_password, "Ncard")
                cursor.execute(sql, val)
                cursor.execute(
                    "SELECT  `user_id` from user WHERE username = %s", (username,))
                user_id = cursor.fetchone()
                payload = {
                    "user_id":  user_id["user_id"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
                }
                token = jwt.encode(payload, config(
                    "secret_key"), algorithm='HS256')
                res = make_response(jsonify({"ok": True}), 200)
                res.set_cookie('token', token, expires=datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=180))
                return res

        else:
            if user["signintype"] == "Google":
                payload = {
                    "user_id": user["user_id"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
                }
                token = jwt.encode(payload, config(
                    "secret_key"), algorithm='HS256')
                res = make_response(jsonify({"ok": True}), 200)
                res.set_cookie('token', token, expires=datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=180))
                return res

            elif user["signintype"] == "FB":
                payload = {
                    "user_id": user["user_id"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
                }
                token = jwt.encode(payload, config(
                    "secret_key"), algorithm='HS256')
                res = make_response(jsonify({"ok": True}), 200)
                res.set_cookie('token', token, expires=datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=180))
                return res
            else:
                check_password = bcrypt.check_password_hash(
                    user["password"], password)
                if check_password:
                    payload = {
                        "user_id": user["user_id"],
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
                    }
                    token = jwt.encode(payload, config(
                        "secret_key"), algorithm='HS256')
                    res = make_response(
                        jsonify({"data": user["username"]}), 200)
                    # res.delete_cookie("unconfirmed")
                    res.set_cookie('token', token, expires=datetime.datetime.utcnow(
                    ) + datetime.timedelta(minutes=180))
                    return res
                else:
                    res = make_response(
                        jsonify({"error": True, "message": "登入失敗,請重新嘗試"}), 400)
                    return res

    # except:
    #     db.rollback()
    #     # res = make_response(
    #     #     jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
    #     # return res
    finally:
        db.commit()
        db.close()


@user_blueprint.route("/api/user", methods=["GET"])
def get_user():
    token = request.cookies.get('token')
    if token is not None:
        userdata = jwt.decode(token.encode('UTF-8'),
                              config("secret_key"), algorithms=["HS256"])
        # print(userdata)
        return {"ok": True}
    else:
        return jsonify({"data": None})


# @user_blueprint.route("/confirm/<token>")
# def confirm_email(token):
#     try:
#         email = confirm_token(token)
#         db = con_pool.get_connection()
#         cursor = db.cursor(dictionary=True)
#         cursor.execute(
#             "SELECT  * from unconfirmeduser WHERE email = %s", (email,))
#         user = cursor.fetchone()
#         if user is not None:
#             cursor.execute("Insert Into user(username ,password) Values( %s ,%s)",
#                            (user["email"], user["password"]))
#             cursor.execute(
#                 "DELETE FROM unconfirmeduser WHERE email = %s", (email,))
#             db.commit()
#             res = make_response(redirect(url_for('confirmed')))
#             return res
#         else:
#             return {"error": True, "message": "註冊失敗，請重新註冊"}
#     except SignatureExpired:
#         return "驗證失效"
#     except:
#         db.rollback()
#     finally:
#         db.close()


# @ user_blueprint.route("/api/unconfirmed")
# def unconfirmed():
#     unconfirmed = request.cookies.get('unconfirmed')
#     if unconfirmed is not None:
#         data = jwt.decode(unconfirmed.encode('UTF-8'),
#                           config("secret_key"), algorithms=["HS256"])
#         # print(data)
#         return {"data": {"Email": data["user_email"]}}
#     else:
#         return {"data": None}

@user_blueprint.route("/api/user", methods=["DELETE"])
def delete_user():
    res = make_response(jsonify({"ok": True}), 200)
    # res.delete_cookie("token")
    res.set_cookie('token', expires=0)
    return res